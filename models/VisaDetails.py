from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class VisaStatusBase(BaseModel):
    visa_status: str = Field(
        ...,
        description="Current visa type/status.",
        json_schema_extra={"example": "F1"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"visa_status": "F1"},
                {"visa_status": "H1B"},
                {"visa_status": "OPT"},
            ]
        }
    }


class VisaStatusCreate(VisaStatusBase):
    """Creation payload for Visa Status."""
    model_config = {
        "json_schema_extra": {
            "examples": [{"visa_status": "F1"}]
        }
    }


class VisaStatusUpdate(BaseModel):
    """Partial update for Visa Status; supply only fields to change."""
    visa_status: Optional[str] = Field(
        None, description="Visa status.", json_schema_extra={"example": "OPT"}
    )

    model_config = {
        "json_schema_extra": {
            "examples": [{"visa_status": "OPT"}]
        }
    }


class VisaStatusRead(VisaStatusBase):
    """Server representation returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Visa Status ID.",
        json_schema_extra={"example": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"},
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
                    "visa_status": "F1",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
