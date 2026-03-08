"""
Playbooks Router
================
Playbook management endpoints.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from src.middleware.tenant_context import TenantContext, get_tenant_context

router = APIRouter()


# Request/Response Models
class PlaybookResponse(BaseModel):
    """Playbook response."""

    id: str
    tenant_id: str
    name: str
    description: Optional[str]
    is_default: bool
    version: int
    created_by: Optional[str]
    created_at: str
    updated_at: str


class PlaybookCreate(BaseModel):
    """Playbook creation request."""

    name: str
    description: Optional[str] = None
    is_default: bool = False


class PlaybookUpdate(BaseModel):
    """Playbook update request."""

    name: Optional[str] = None
    description: Optional[str] = None
    is_default: Optional[bool] = None


class PlaybookRuleResponse(BaseModel):
    """Playbook rule response."""

    id: str
    playbook_id: str
    category: str
    priority: str
    preferred: dict
    acceptable: dict
    unacceptable: dict
    rationale: Optional[str]
    created_at: str
    updated_at: str


class PlaybookRuleCreate(BaseModel):
    """Playbook rule creation request."""

    category: str
    priority: str = "standard"
    preferred: dict
    acceptable: dict
    unacceptable: dict = {}
    rationale: Optional[str] = None


class PlaybookRuleUpdate(BaseModel):
    """Playbook rule update request."""

    priority: Optional[str] = None
    preferred: Optional[dict] = None
    acceptable: Optional[dict] = None
    unacceptable: Optional[dict] = None
    rationale: Optional[str] = None


@router.get("", response_model=list[PlaybookResponse])
async def list_playbooks(
    ctx: TenantContext = Depends(get_tenant_context),
):
    """
    List all playbooks for the current tenant.
    """
    from src.database.session import get_db_session

    async with get_db_session() as session:
        result = await session.execute(
            """
            SELECT id, tenant_id, name, description, is_default, version,
                   created_by, created_at, updated_at
            FROM playbooks
            WHERE tenant_id = :tenant_id
            ORDER BY is_default DESC, name
            """,
            {"tenant_id": ctx.tenant_id},
        )
        rows = result.fetchall()

    return [
        PlaybookResponse(
            id=row.id,
            tenant_id=row.tenant_id,
            name=row.name,
            description=row.description,
            is_default=row.is_default,
            version=row.version,
            created_by=row.created_by,
            created_at=row.created_at.isoformat(),
            updated_at=row.updated_at.isoformat(),
        )
        for row in rows
    ]


@router.post("", response_model=PlaybookResponse, status_code=201)
async def create_playbook(
    request: PlaybookCreate,
    ctx: TenantContext = Depends(get_tenant_context),
):
    """
    Create a new playbook.
    """
    import uuid
    from src.database.session import get_db_session

    playbook_id = str(uuid.uuid4())

    async with get_db_session() as session:
        # If setting as default, unset other defaults
        if request.is_default:
            await session.execute(
                """
                UPDATE playbooks
                SET is_default = false
                WHERE tenant_id = :tenant_id
                """,
                {"tenant_id": ctx.tenant_id},
            )

        await session.execute(
            """
            INSERT INTO playbooks
            (id, tenant_id, name, description, is_default, version, created_by, created_at, updated_at)
            VALUES (:id, :tenant_id, :name, :description, :is_default, 1, :user_id, NOW(), NOW())
            """,
            {
                "id": playbook_id,
                "tenant_id": ctx.tenant_id,
                "name": request.name,
                "description": request.description,
                "is_default": request.is_default,
                "user_id": ctx.user_id,
            },
        )

        await session.commit()

    return PlaybookResponse(
        id=playbook_id,
        tenant_id=ctx.tenant_id,
        name=request.name,
        description=request.description,
        is_default=request.is_default,
        version=1,
        created_by=ctx.user_id,
        created_at="",
        updated_at="",
    )


@router.get("/{playbook_id}", response_model=PlaybookResponse)
async def get_playbook(
    playbook_id: str,
    ctx: TenantContext = Depends(get_tenant_context),
):
    """
    Get a specific playbook.
    """
    from src.database.session import get_db_session

    async with get_db_session() as session:
        result = await session.execute(
            """
            SELECT id, tenant_id, name, description, is_default, version,
                   created_by, created_at, updated_at
            FROM playbooks
            WHERE id = :playbook_id AND tenant_id = :tenant_id
            """,
            {"playbook_id": playbook_id, "tenant_id": ctx.tenant_id},
        )
        row = result.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Playbook not found")

    return PlaybookResponse(
        id=row.id,
        tenant_id=row.tenant_id,
        name=row.name,
        description=row.description,
        is_default=row.is_default,
        version=row.version,
        created_by=row.created_by,
        created_at=row.created_at.isoformat(),
        updated_at=row.updated_at.isoformat(),
    )


@router.patch("/{playbook_id}", response_model=PlaybookResponse)
async def update_playbook(
    playbook_id: str,
    request: PlaybookUpdate,
    ctx: TenantContext = Depends(get_tenant_context),
):
    """
    Update a playbook.
    """
    import uuid
    from src.database.session import get_db_session

    async with get_db_session() as session:
        # Check ownership
        result = await session.execute(
            """
            SELECT id FROM playbooks
            WHERE id = :playbook_id AND tenant_id = :tenant_id
            """,
            {"playbook_id": playbook_id, "tenant_id": ctx.tenant_id},
        )

        if not result.fetchone():
            raise HTTPException(status_code=404, detail="Playbook not found")

        # Build update
        update_fields = ["version = version + 1", "updated_at = NOW()"]
        params = {"playbook_id": playbook_id}

        if request.name is not None:
            update_fields.append("name = :name")
            params["name"] = request.name

        if request.description is not None:
            update_fields.append("description = :description")
            params["description"] = request.description

        if request.is_default is not None:
            # Unset other defaults if setting this one as default
            if request.is_default:
                await session.execute(
                    """
                    UPDATE playbooks
                    SET is_default = false
                    WHERE tenant_id = :tenant_id AND id != :playbook_id
                    """,
                    {"tenant_id": ctx.tenant_id, "playbook_id": playbook_id},
                )
            update_fields.append("is_default = :is_default")
            params["is_default"] = request.is_default

        await session.execute(
            f"UPDATE playbooks SET {', '.join(update_fields)} WHERE id = :playbook_id",
            params,
        )

        await session.commit()

    return await get_playbook(playbook_id, ctx)


@router.delete("/{playbook_id}")
async def delete_playbook(
    playbook_id: str,
    ctx: TenantContext = Depends(get_tenant_context),
):
    """
    Delete a playbook.
    """
    from src.database.session import get_db_session

    async with get_db_session() as session:
        # Check ownership
        result = await session.execute(
            """
            SELECT id FROM playbooks
            WHERE id = :playbook_id AND tenant_id = :tenant_id
            """,
            {"playbook_id": playbook_id, "tenant_id": ctx.tenant_id},
        )

        if not result.fetchone():
            raise HTTPException(status_code=404, detail="Playbook not found")

        # Delete rules first
        await session.execute(
            "DELETE FROM playbook_rules WHERE playbook_id = :playbook_id",
            {"playbook_id": playbook_id},
        )

        # Delete playbook
        await session.execute(
            "DELETE FROM playbooks WHERE id = :playbook_id",
            {"playbook_id": playbook_id},
        )

        await session.commit()

    return {"message": "Playbook deleted"}


# Playbook Rules
@router.get("/{playbook_id}/rules", response_model=list[PlaybookRuleResponse])
async def list_playbook_rules(
    playbook_id: str,
    ctx: TenantContext = Depends(get_tenant_context),
    category: Optional[str] = None,
):
    """
    List rules for a playbook.
    """
    from src.database.session import get_db_session

    async with get_db_session() as session:
        # Verify playbook ownership
        result = await session.execute(
            """
            SELECT id FROM playbooks
            WHERE id = :playbook_id AND tenant_id = :tenant_id
            """,
            {"playbook_id": playbook_id, "tenant_id": ctx.tenant_id},
        )

        if not result.fetchone():
            raise HTTPException(status_code=404, detail="Playbook not found")

        # Get rules
        query = """
            SELECT id, playbook_id, category, priority, preferred, acceptable,
                   unacceptable, rationale, created_at, updated_at
            FROM playbook_rules
            WHERE playbook_id = :playbook_id
        """
        params = {"playbook_id": playbook_id}

        if category:
            query += " AND category = :category"
            params["category"] = category

        result = await session.execute(query, params)
        rows = result.fetchall()

    return [
        PlaybookRuleResponse(
            id=row.id,
            playbook_id=row.playbook_id,
            category=row.category,
            priority=row.priority,
            preferred=row.preferred or {},
            acceptable=row.acceptable or {},
            unacceptable=row.unacceptable or {},
            rationale=row.rationale,
            created_at=row.created_at.isoformat(),
            updated_at=row.updated_at.isoformat(),
        )
        for row in rows
    ]


@router.post("/{playbook_id}/rules", response_model=PlaybookRuleResponse, status_code=201)
async def create_playbook_rule(
    playbook_id: str,
    request: PlaybookRuleCreate,
    ctx: TenantContext = Depends(get_tenant_context),
):
    """
    Add a rule to a playbook.
    """
    import uuid
    from src.database.session import get_db_session

    rule_id = str(uuid.uuid4())

    async with get_db_session() as session:
        # Verify playbook ownership
        result = await session.execute(
            """
            SELECT id FROM playbooks
            WHERE id = :playbook_id AND tenant_id = :tenant_id
            """,
            {"playbook_id": playbook_id, "tenant_id": ctx.tenant_id},
        )

        if not result.fetchone():
            raise HTTPException(status_code=404, detail="Playbook not found")

        await session.execute(
            """
            INSERT INTO playbook_rules
            (id, playbook_id, category, priority, preferred, acceptable, unacceptable, rationale, created_at, updated_at)
            VALUES (:id, :playbook_id, :category, :priority, :preferred, :acceptable, :unacceptable, :rationale, NOW(), NOW())
            """,
            {
                "id": rule_id,
                "playbook_id": playbook_id,
                "category": request.category,
                "priority": request.priority,
                "preferred": request.preferred,
                "acceptable": request.acceptable,
                "unacceptable": request.unacceptable,
                "rationale": request.rationale,
            },
        )

        await session.commit()

    return PlaybookRuleResponse(
        id=rule_id,
        playbook_id=playbook_id,
        category=request.category,
        priority=request.priority,
        preferred=request.preferred,
        acceptable=request.acceptable,
        unacceptable=request.unacceptable,
        rationale=request.rationale,
        created_at="",
        updated_at="",
    )


@router.patch("/{playbook_id}/rules/{rule_id}", response_model=PlaybookRuleResponse)
async def update_playbook_rule(
    playbook_id: str,
    rule_id: str,
    request: PlaybookRuleUpdate,
    ctx: TenantContext = Depends(get_tenant_context),
):
    """
    Update a playbook rule.
    """
    from src.database.session import get_db_session

    async with get_db_session() as session:
        # Verify ownership
        result = await session.execute(
            """
            SELECT r.id FROM playbook_rules r
            JOIN playbooks p ON r.playbook_id = p.id
            WHERE r.id = :rule_id AND r.playbook_id = :playbook_id AND p.tenant_id = :tenant_id
            """,
            {"rule_id": rule_id, "playbook_id": playbook_id, "tenant_id": ctx.tenant_id},
        )

        if not result.fetchone():
            raise HTTPException(status_code=404, detail="Rule not found")

        # Build update
        update_fields = ["updated_at = NOW()"]
        params = {"rule_id": rule_id}

        for field, value in [
            ("priority", request.priority),
            ("preferred", request.preferred),
            ("acceptable", request.acceptable),
            ("unacceptable", request.unacceptable),
            ("rationale", request.rationale),
        ]:
            if value is not None:
                update_fields.append(f"{field} = :{field}")
                params[field] = value

        await session.execute(
            f"UPDATE playbook_rules SET {', '.join(update_fields)} WHERE id = :rule_id",
            params,
        )

        await session.commit()

    return {"message": "Rule updated"}


@router.delete("/{playbook_id}/rules/{rule_id}")
async def delete_playbook_rule(
    playbook_id: str,
    rule_id: str,
    ctx: TenantContext = Depends(get_tenant_context),
):
    """
    Delete a playbook rule.
    """
    from src.database.session import get_db_session

    async with get_db_session() as session:
        result = await session.execute(
            """
            SELECT r.id FROM playbook_rules r
            JOIN playbooks p ON r.playbook_id = p.id
            WHERE r.id = :rule_id AND r.playbook_id = :playbook_id AND p.tenant_id = :tenant_id
            """,
            {"rule_id": rule_id, "playbook_id": playbook_id, "tenant_id": ctx.tenant_id},
        )

        if not result.fetchone():
            raise HTTPException(status_code=404, detail="Rule not found")

        await session.execute(
            "DELETE FROM playbook_rules WHERE id = :rule_id",
            {"rule_id": rule_id},
        )

        await session.commit()

    return {"message": "Rule deleted"}
