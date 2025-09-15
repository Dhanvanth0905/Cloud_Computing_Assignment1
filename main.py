from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.person import PersonCreate, PersonRead, PersonUpdate
from models.address import AddressCreate, AddressRead, AddressUpdate
from models.health import Health
from models.FeeDetails import FeeDetailsCreate, FeeDetailsRead, FeeDetailsUpdate
from models.VisaDetails import VisaStatusCreate, VisaStatusRead, VisaStatusUpdate   # <<< NEW >>>

port = int(os.environ.get("FASTAPIPORT", 8000))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------
persons: Dict[UUID, PersonRead] = {}
addresses: Dict[UUID, AddressRead] = {}
fee_details: Dict[UUID, FeeDetailsRead] = {}
visa_statuses: Dict[UUID, VisaStatusRead] = {}   # <<< NEW >>>

app = FastAPI(
    title="Person/Address/FeeDetails/VisaStatus API",   # <<< MODIFIED >>>
    description="Demo FastAPI app using Pydantic v2 models for Person, Address, FeeDetails, and VisaStatus",  # <<< MODIFIED >>>
    version="0.1.0",
)

# -----------------------------------------------------------------------------
# Health endpoints
# -----------------------------------------------------------------------------
def make_health(echo: Optional[str], path_echo: Optional[str]=None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo
    )

@app.get("/health", response_model=Health)
def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
    return make_health(echo=echo, path_echo=None)

@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)

# -----------------------------------------------------------------------------
# Address endpoints (unchanged)
# -----------------------------------------------------------------------------
@app.post("/addresses", response_model=AddressRead, status_code=201)
def create_address(address: AddressCreate):
    if address.id in addresses:
        raise HTTPException(status_code=400, detail="Address with this ID already exists")
    addresses[address.id] = AddressRead(**address.model_dump())
    return addresses[address.id]

@app.get("/addresses", response_model=List[AddressRead])
def list_addresses(
    street: Optional[str] = Query(None, description="Filter by street"),
    city: Optional[str] = Query(None, description="Filter by city"),
    state: Optional[str] = Query(None, description="Filter by state/region"),
    postal_code: Optional[str] = Query(None, description="Filter by postal code"),
    country: Optional[str] = Query(None, description="Filter by country"),
):
    results = list(addresses.values())
    if street is not None:
        results = [a for a in results if a.street == street]
    if city is not None:
        results = [a for a in results if a.city == city]
    if state is not None:
        results = [a for a in results if a.state == state]
    if postal_code is not None:
        results = [a for a in results if a.postal_code == postal_code]
    if country is not None:
        results = [a for a in results if a.country == country]
    return results

@app.get("/addresses/{address_id}", response_model=AddressRead)
def get_address(address_id: UUID):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    return addresses[address_id]

@app.patch("/addresses/{address_id}", response_model=AddressRead)
def update_address(address_id: UUID, update: AddressUpdate):
    if address_id not in addresses:
        raise HTTPException(status_code=404, detail="Address not found")
    stored = addresses[address_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    addresses[address_id] = AddressRead(**stored)
    return addresses[address_id]

# -----------------------------------------------------------------------------
# Person endpoints (unchanged)
# -----------------------------------------------------------------------------
@app.post("/persons", response_model=PersonRead, status_code=201)
def create_person(person: PersonCreate):
    person_read = PersonRead(**person.model_dump())
    persons[person_read.id] = person_read
    return person_read

@app.get("/persons", response_model=List[PersonRead])
def list_persons(
    uni: Optional[str] = Query(None, description="Filter by Columbia UNI"),
    first_name: Optional[str] = Query(None, description="Filter by first name"),
    last_name: Optional[str] = Query(None, description="Filter by last name"),
    email: Optional[str] = Query(None, description="Filter by email"),
    phone: Optional[str] = Query(None, description="Filter by phone number"),
    birth_date: Optional[str] = Query(None, description="Filter by date of birth (YYYY-MM-DD)"),
    city: Optional[str] = Query(None, description="Filter by city of at least one address"),
    country: Optional[str] = Query(None, description="Filter by country of at least one address"),
):
    results = list(persons.values())
    if uni is not None:
        results = [p for p in results if p.uni == uni]
    if first_name is not None:
        results = [p for p in results if p.first_name == first_name]
    if last_name is not None:
        results = [p for p in results if p.last_name == last_name]
    if email is not None:
        results = [p for p in results if p.email == email]
    if phone is not None:
        results = [p for p in results if p.phone == phone]
    if birth_date is not None:
        results = [p for p in results if str(p.birth_date) == birth_date]
    if city is not None:
        results = [p for p in results if any(addr.city == city for addr in p.addresses)]
    if country is not None:
        results = [p for p in results if any(addr.country == country for addr in p.addresses)]
    return results

@app.get("/persons/{person_id}", response_model=PersonRead)
def get_person(person_id: UUID):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    return persons[person_id]

@app.patch("/persons/{person_id}", response_model=PersonRead)
def update_person(person_id: UUID, update: PersonUpdate):
    if person_id not in persons:
        raise HTTPException(status_code=404, detail="Person not found")
    stored = persons[person_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    persons[person_id] = PersonRead(**stored)
    return persons[person_id]

# -----------------------------------------------------------------------------
# FeeDetails endpoints (unchanged)
# -----------------------------------------------------------------------------
@app.post("/fee_details", response_model=FeeDetailsRead, status_code=201)
def create_fee_details(fee: FeeDetailsCreate):
    fee_read = FeeDetailsRead(**fee.model_dump())
    fee_details[fee_read.id] = fee_read
    return fee_read

@app.get("/fee_details", response_model=List[FeeDetailsRead])
def list_fee_details(
    university_name: Optional[str] = Query(None, description="Filter by university name"),
    fee_paid: Optional[bool] = Query(None, description="Filter by fee payment status"),
):
    results = list(fee_details.values())
    if university_name is not None:
        results = [f for f in results if f.university_name == university_name]
    if fee_paid is not None:
        results = [f for f in results if f.fee_paid == fee_paid]
    return results

@app.get("/fee_details/{fee_id}", response_model=FeeDetailsRead)
def get_fee_details(fee_id: UUID):
    if fee_id not in fee_details:
        raise HTTPException(status_code=404, detail="FeeDetails not found")
    return fee_details[fee_id]

@app.patch("/fee_details/{fee_id}", response_model=FeeDetailsRead)
def update_fee_details(fee_id: UUID, update: FeeDetailsUpdate):
    if fee_id not in fee_details:
        raise HTTPException(status_code=404, detail="FeeDetails not found")
    stored = fee_details[fee_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    fee_details[fee_id] = FeeDetailsRead(**stored)
    return fee_details[fee_id]

# -----------------------------------------------------------------------------
# VisaStatus endpoints  <<< NEW >>>
# -----------------------------------------------------------------------------
@app.post("/visa_status", response_model=VisaStatusRead, status_code=201)
def create_visa_status(visa: VisaStatusCreate):
    visa_read = VisaStatusRead(**visa.model_dump())
    visa_statuses[visa_read.id] = visa_read
    return visa_read

@app.get("/visa_status", response_model=List[VisaStatusRead])
def list_visa_statuses(
    visa_status: Optional[str] = Query(None, description="Filter by visa status"),
):
    results = list(visa_statuses.values())
    if visa_status is not None:
        results = [v for v in results if v.visa_status == visa_status]
    return results

@app.get("/visa_status/{visa_id}", response_model=VisaStatusRead)
def get_visa_status(visa_id: UUID):
    if visa_id not in visa_statuses:
        raise HTTPException(status_code=404, detail="VisaStatus not found")
    return visa_statuses[visa_id]

@app.patch("/visa_status/{visa_id}", response_model=VisaStatusRead)
def update_visa_status(visa_id: UUID, update: VisaStatusUpdate):
    if visa_id not in visa_statuses:
        raise HTTPException(status_code=404, detail="VisaStatus not found")
    stored = visa_statuses[visa_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    visa_statuses[visa_id] = VisaStatusRead(**stored)
    return visa_statuses[visa_id]

# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Person/Address/FeeDetails/VisaStatus API. See /docs for OpenAPI UI."}  # <<< MODIFIED >>>

# -----------------------------------------------------------------------------
# Entrypoint
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
