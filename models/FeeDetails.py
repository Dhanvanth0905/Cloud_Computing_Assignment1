from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class FeeDetailsBase(BaseModel):
    university_name: str = Field(
        ...,
        description="Name of the university.",
        json_schema_extra={"example": "Columbia University"},
    )
    number_of_credits: int = Field(
        ...,
        description="Total number of credits registered for the program.",
        json_schema_extra={"example": 30},
    )
    fee_paid: bool = Field(
        ...,
        description="Whether the tuition fee has been paid.",
        json_schema_extra={"example": True},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "university_name": "Columbia University",
                    "number_of_credits": 30,
                    "fee_paid": True,
                }
            ]
        }
    }


class FeeDetailsCreate(FeeDetailsBase):
    """Creation payload for Fee Details."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "university_name": "Columbia University",
                    "number_of_credits": 30,
                    "fee_paid": True,
                }
            ]
        }
    }


class FeeDetailsUpdate(BaseModel):
    """Partial update for Fee Details; supply only fields to change."""
    university_name: Optional[str] = Field(
        None, description="Name of the university.", json_schema_extra={"example": "Columbia University"}
    )
    number_of_credits: Optional[int] = Field(
        None, description="Number of credits.", json_schema_extra={"example": 36}
    )
    fee_paid: Optional[bool] = Field(
        None, description="Fee payment status.", json_schema_extra={"example": False}
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"number_of_credits": 36},
                {"fee_paid": False},
                {"university_name": "New York University"},
            ]
        }
    }


class FeeDetailsRead(FeeDetailsBase):
    """Server representation of Fee Details returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Fee Details ID.",
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
                    "university_name": "Columbia University",
                    "number_of_credits": 30,
                    "fee_paid": True,
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
