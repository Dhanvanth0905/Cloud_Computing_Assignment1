from __future__ import annotations

from typing import Optional, List, Annotated
from uuid import UUID, uuid4
from datetime import date, datetime
from pydantic import BaseModel, Field, EmailStr, StringConstraints

from .address import AddressBase

# Columbia UNI: 2–3 lowercase letters + 1–4 digits (e.g., abc1234)
UNIType = Annotated[str, StringConstraints(pattern=r"^[a-z]{2,3}\d{1,4}$")]


class PersonBase(BaseModel):
    uni: UNIType = Field(
        ...,
        description="Columbia University UNI (2–3 lowercase letters + 1–4 digits).",
        json_schema_extra={"example":"dy2530"},
    )
    first_name: str = Field(
        ...,
        description="Given name.",
        json_schema_extra={"example":"Dhanvanth Reddy"},
    )
    last_name: str = Field(
        ...,
        description="Family name.",
        json_schema_extra={"example":"Yerramreddy"},
    )
    email: EmailStr = Field(
        ...,
        description="Primary email address.",
        json_schema_extra={"example":"dhanvanthyerramreddy09@gmail.com"},
    )
    phone: Optional[str] = Field(
        None,
        description="Contact phone number in any reasonable format.",
        json_schema_extra={"example":"+1-646-408-9482"},
    )
    birth_date: Optional[date] = Field(
        None,
        description="Date of birth (YYYY-MM-DD).",
        json_schema_extra={"example":"2002-05-09"},
    )

    # Embed addresses (each with persistent ID)
    addresses: List[AddressBase] = Field(
        default_factory=list,
        description="Addresses linked to this person (each carries a persistent Address ID).",
        json_schema_extra={
            "example": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "street": "736 Riverside Dr",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10031",
                    "country": "USA",
                }
            ]
        },
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "uni": "dy2530",
                    "first_name": "Dhanvanth Reddy",
                    "last_name": "Yerramreddy",
                    "email": "dhanvanthyerramreddy09@gmail.com",
                    "phone": "+1-646-408-9482",
                    "birth_date": "2002-05-09",
                    "addresses": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "street": "736 Riverside Dr",
                            "city": "New York",
                            "state": "NY",
                            "postal_code": "10031",
                            "country": "USA",
                        }
                    ],
                }
            ]
        }
    }


class PersonCreate(PersonBase):
    """Creation payload for a Person."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "uni": "dy2530",
                    "first_name": "Dhanvanth Reddy",
                    "last_name": "Yerramreddy",
                    "email": "dhanvanthyerramreddy09@gmail.com",
                    "phone": "+1-646-408-9482",
                    "birth_date": "2002-05-09",
                    "addresses": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "street": "736 Riverside Dr",
                            "city": "New York",
                            "state": "NY",
                            "postal_code": "10031",
                            "country": "USA",
                        }
                    ],
                }
            ]
        }
    }


class PersonUpdate(BaseModel):
    """Partial update for a Person; supply only fields to change."""
    uni: Optional[UNIType] = Field(
        None, description="Columbia UNI.", json_schema_extra={"example":"dy2530"}
    )
    first_name: Optional[str] = Field(None, json_schema_extra={"example":"Dhanvanth Reddy"})
    last_name: Optional[str] = Field(None, json_schema_extra={"example":"Yerramreddy"})
    email: Optional[EmailStr] = Field(None, json_schema_extra={"example":"dhanvanthyerramreddy09@gmail.com"})
    phone: Optional[str] = Field(None, json_schema_extra={"example":"+1-646-408-9482"})
    birth_date: Optional[date] = Field(None, json_schema_extra={"example":"2002-05-09"})
    addresses: Optional[List[AddressBase]] = Field(
        None,
        description="Replace the entire set of addresses with this list.",
        json_schema_extra={
            "example": [
                {
                    "id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
                    "street": "736 Riverside Dr",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10031",
                    "country": "USA",
                }
            ]
        },
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"first_name": "Dhanvanth Reddy", "last_name": "Yerramreddy"},
                {"phone": "+1-646-408-9482"},
                {
                    "addresses": [
                        {
                            "id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
                            "street": "736 Riverside Dr",
                            "city": "New York",
                            "state": "NY",
                            "postal_code": "10031",
                            "country": "USA",
                        }
                    ]
                },
            ]
        }
    }


class PersonRead(PersonBase):
    """Server representation returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Person ID.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
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
                    "id": "99999999-9999-4999-8999-999999999999",
                    "uni": "dy2530",
                    "first_name": "Dhanvanth Reddy",
                    "last_name": "Yerramreddy",
                    "email": "dhanvanthyerramreddy09@gmail.com",
                    "phone": "+1-646-408-9482",
                    "birth_date": "2002-05-09",
                    "addresses": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "street": "736 Riverside Dr",
                            "city": "New York",
                            "state": "NY",
                            "postal_code": "10031",
                            "country": "USA",
                        }
                    ],
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
