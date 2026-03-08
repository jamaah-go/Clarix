"""
Tenant Context Middleware
========================
Extracts and validates tenant context from JWT tokens.
"""
from typing import Callable
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError, jwt
from pydantic import BaseModel

from config import get_settings

settings = get_settings()
security = HTTPBearer()


class TenantContext(BaseModel):
    """Tenant context extracted from JWT."""

    tenant_id: str
    user_id: str
    email: str
    role: str
    plan_tier: str = "starter"


def extract_tenant_context(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> TenantContext:
    """
    Extract and validate tenant context from JWT token.
    Used as a FastAPI dependency.
    """
    token = credentials.credentials

    try:
        # Decode JWT
        payload = jwt.decode(
            token,
            settings.supabase_jwt_secret,
            algorithms=[settings.algorithm],
        )

        # Validate required claims
        tenant_id = payload.get("tenant_id")
        user_id = payload.get("sub")
        email = payload.get("email")
        role = payload.get("role", "member")
        plan_tier = payload.get("plan_tier", "starter")

        if not tenant_id or not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid token: missing required claims",
            )

        return TenantContext(
            tenant_id=tenant_id,
            user_id=user_id,
            email=email or "",
            role=role,
            plan_tier=plan_tier,
        )

    except JWTError as e:
        raise HTTPException(
            status_code=401,
            detail=f"Invalid token: {str(e)}",
        )


def get_tenant_context(
    context: TenantContext = Depends(extract_tenant_context),
) -> TenantContext:
    """Dependency to get tenant context."""
    return context


class TenantContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware to extract tenant context from Authorization header.
    Makes context available in request.state for downstream handlers.
    """

    EXCLUDED_PATHS = [
        "/",
        "/api/docs",
        "/api/redoc",
        "/api/v1/health",
        "/api/v1/auth/login",
        "/api/v1/auth/register",
        "/api/v1/webhooks/stripe",
    ]

    async def dispatch(self, request: Request, call_next):
        # Skip excluded paths
        if request.url.path in self.EXCLUDED_PATHS or request.url.path.startswith(
            "/api/v1/auth/"
        ):
            return await call_next(request)

        # Skip if no Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            # Let the dependency handle the error
            return await call_next(request)

        # Extract token
        token = auth_header.replace("Bearer ", "")

        try:
            # Decode JWT
            payload = jwt.decode(
                token,
                settings.supabase_jwt_secret,
                algorithms=[settings.algorithm],
            )

            # Set tenant context in request state
            request.state.tenant_id = payload.get("tenant_id")
            request.state.user_id = payload.get("sub")
            request.state.user_email = payload.get("email")
            request.state.user_role = payload.get("role", "member")
            request.state.plan_tier = payload.get("plan_tier", "starter")

        except JWTError:
            # Let the dependency handle the error
            pass

        return await call_next(request)
