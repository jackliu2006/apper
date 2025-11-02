import os
from enum import Enum
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum as SQLAEnum, create_engine, Boolean
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from .database import Base,DB_SESSION


class CountryEnum(str, Enum):
    """Valid country codes"""
    DE = "Germany"
    CN = "China"
    CH = "Switzerland"


class AddressModel(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    street = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    postalCode = Column(String, nullable=False)
    country = Column(SQLAEnum(CountryEnum), nullable=False)
    isPrimary = Column(Boolean, default=False)
    customerId = Column(Integer, ForeignKey("customers.id"), nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow)

    # Relationship to Customer
    customer = relationship("CustomerModel", back_populates="addresses")


class Address(BaseModel):
    """Address is one of addresses of a customer"""
    id: int
    street: str
    city: str
    state: Optional[str] = None
    postalCode: str
    country: CountryEnum
    isPrimary: bool
    customerId: int
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

def create_address(address_data: Address) -> Address:
    """Create a new address in the database
    
    Args:
        address_data (Address): The address data to create
        
    Returns:
        AddressRead: The created address with database-populated fields
    """
    db_address = AddressModel(
        street=address_data.street,
        city=address_data.city,
        state=address_data.state,
        postalCode=address_data.postalCode,
        country=address_data.country,
        isPrimary=address_data.isPrimary,
        customerId=address_data.customerId,
        createdAt=datetime.utcnow(),
        updatedAt=datetime.utcnow()
    )
    DB_SESSION.add(db_address)
    DB_SESSION.commit()
    DB_SESSION.refresh(db_address)
    return Address.model_validate(db_address)

def get_all_addresses() -> List[Address]:
    """Retrieve all addresses from the database
    
    Returns:
        List[Address]: List of all addresses in the database
    """
    addresses = DB_SESSION.query(AddressModel).all()
    return [Address.model_validate(addr) for addr in addresses]

def get_address_by_id(address_id: int) -> Optional[Address]:
    """Retrieve an address by its ID
    
    Args:
        address_id (int): The ID of the address to retrieve
        
    Returns:
        Optional[Address]: The address if found, None otherwise
    """
    address = DB_SESSION.query(AddressModel).filter(AddressModel.id == address_id).first()
    return Address.model_validate(address) if address else None

def get_addresses_by_customer(customer_id: int) -> List[Address]:
    """Retrieve all addresses for a specific customer
    
    Args:
        customer_id (int): The ID of the customer
        
    Returns:
        List[AddressRead]: List of all addresses for the customer
    """
    addresses = DB_SESSION.query(AddressModel).filter(AddressModel.customerId == customer_id).all()
    return [Address.model_validate(addr) for addr in addresses]