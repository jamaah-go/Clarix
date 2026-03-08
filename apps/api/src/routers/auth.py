"""
Authentication Router
====================
User registration, login, and token management.
"""
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from jose import jwt
import hashlib

from config import get_settings

router = APIRouter()
settings = get_settings()
security = HTTPBearer()


# Request/Response Models
class LoginRequest(BaseModel):
    """Login request."""

    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    """Registration request."""

    email: EmailStr
    password: str
    full_name: Optional[str] = None
    tenant_name: Optional[str] = None


class AuthResponse(BaseModel):
    """Authentication response."""

    access_token: str
    token_type: str
    expires_in: int
    user: "UserInfo"


class UserInfo(BaseModel):
    """User information."""

    id: str
    email: str
    full_name: Optional[str]
    tenant_id: str
    role: str
    plan_tier: str


class PasswordResetRequest(BaseModel):
    """Password reset request."""

    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Password reset confirmation."""

    token: str
    new_password: str


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest):
    """
    Register a new user and tenant.
    """
    from src.database.session import get_db_session

    # Create tenant
    tenant_id = str(hashlib.sha256(request.tenant_name or request.email).hexdigest())[:8]

    async with get_db_session() as session:
        # Check if email exists
        result = await session.execute(
            "SELECT id FROM users WHERE email = :email",
            {"email": request.email},
        )
        if result.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # Create tenant
        await session.execute(
            """
            INSERT INTO tenants (id, name, slug, plan_tier, created_at, updated_at)
            VALUES (:id, :name, :slug, 'starter', NOW(), NOW())
            """,
            {
                "id": tenant_id,
                "name": request.tenant_name or f"{request.email}'s Organization",
                "slug": request.tenant_name or tenant_id,
            },
        )

        # Create user
        user_id = str(hashlib.sha256(request.email.encode()).hexdigest())[:16]
        password_hash = hashlib.sha256(request.password.encode()).hexdigest()

        await session.execute(
            """
            INSERT INTO users (id, tenant_id, email, full_name, role, password_hash, created_at, updated_at)
            VALUES (:id, :tenant_id, :email, :full_name, 'admin', :password_hash, NOW(), NOW())
            """,
            {
                "id": user_id,
                "tenant_id": tenant_id,
                "email": request.email,
                "full_name": request.full_name,
                "password_hash": password_hash,
            },
        )

        await session.commit()

    # Generate token
    token = await _create_access_token(
        user_id=user_id,
        tenant_id=tenant_id,
        email=request.email,
        role="admin",
        plan_tier="starter",
    )

    return AuthResponse(
        access_token=token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60,
        user=UserInfo(
            id=user_id,
            email=request.email,
            full_name=request.full_name,
            tenant_id=tenant_id,
            role="admin",
            plan_tier="starter",
        ),
    )


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest):
    """
    Authenticate user and return JWT token.
    """
    from src.database.session import get_db_session

    password_hash = hashlib.sha256(request.password.encode()).hexdigest()

    async with get_db_session() as session:
        result = await session.execute(
            """
            SELECT id, tenant_id, email, full_name, role, password_hash
            FROM users
            WHERE email = :email
            """,
            {"email": request.email},
        )
        user = result.fetchone()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if user.password_hash != password_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # Get tenant plan tier
        tenant_result = await session.execute(
            "SELECT plan_tier FROM tenants WHERE id = :tenant_id",
            {"tenant_id": user.tenant_id},
        )
        tenant = tenant_result.fetchone()
        plan_tier = tenant.plan_tier if tenant else "starter"

    # Generate token
    token = await _create_access_token(
        user_id=user.id,
        tenant_id=user.tenant_id,
        email=user.email,
        role=user.role,
        plan_tier=plan_tier,
    )

    return AuthResponse(
        access_token=token,
        token_type="bearer",
        expires_in=settings.access_token_expire_minutes * 60,
        user=UserInfo(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            tenant_id=user.tenant_id,
            role=user.role,
            plan_tier=plan_tier,
        ),
    )


@router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Logout user (client should discard token).
    """
    # In a production system, you might want to blacklist the token
    return {"message": "Successfully logged out"}


@router.post("/password-reset")
async def request_password_reset(request: PasswordResetRequest):
    """
    Request password reset email.
    """
    # In production, this would send an email with reset link
    return {"message": "If the email exists, a password reset link has been sent"}


@router.post("/password-reset/confirm")
async def confirm_password_reset(request: PasswordResetConfirm):
    """
    Confirm password reset with token.
    """
    # In production, verify token and update password
    return {"message": "Password has been reset"}


async def _create_access_token(
    user_id: str,
    tenant_id: str,
    email: str,
    role: str,
    plan_tier: str,
) -> str:
    """Create JWT access token."""
    expires = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    payload = {
        "sub": user_id,
        "tenant_id": tenant_id,
        "email": email,
        "role": role,
        "plan_tier": plan_tier,
        "exp": expires,
    }

    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


# Update forward reference
AuthResponse.model_rebuild()
