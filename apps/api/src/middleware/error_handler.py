"""
Error Handler Middleware
=======================
Centralized error handling and response formatting.
"""
import uuid
import traceback
from typing import Callable
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.logging_config import get_logger

logger = get_logger("error_handler")


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Middleware for handling errors consistently across the application."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Add request ID to state for tracking
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Add request ID to response headers
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        return response


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Handle HTTP exceptions."""
    logger.warning(
        "http_exception",
        path=request.url.path,
        method=request.method,
        status_code=exc.status_code,
        detail=exc.detail,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.detail or "HTTP_ERROR",
            "message": exc.detail,
            "request_id": getattr(request.state, "request_id", None),
        },
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unhandled exceptions."""
    logger.exception(
        "unhandled_exception",
        path=request.url.path,
        method=request.method,
        error=str(exc),
        traceback=traceback.format_exc(),
    )

    # Don't expose internal errors in production
    message = (
        "An internal error occurred"
        if not getattr(request.app.state, "settings", None)?.is_development
        else str(exc)
    )

    return JSONResponse(
        status_code=500,
        content={
            "code": "INTERNAL_ERROR",
            "message": message,
            "request_id": getattr(request.state, "request_id", None),
        },
    )
