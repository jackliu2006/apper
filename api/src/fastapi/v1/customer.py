from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLAEnum, create_engine, Boolean
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from .address import Address, AddressModel 
from .contract import Contract, ContractModel
from .database import Base, DB_SESSION



class CustomerModel(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    mobileNumber = Column(String, nullable=True)
    email = Column(String, nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    addresses = relationship(AddressModel, back_populates="customer")
   # contracts = relationship(ContractModel, back_populates="customer")


class Customer(BaseModel):
    """A customer model with personal information, timestamps, and related addresses"""
    id: int
    firstName: str
    lastName: str
    mobileNumber: Optional[str] = None
    email: Optional[str] = None
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None
    addresses: List[Address] = []  # Will contain address data
    #contracts: List[Contract] = []  # Will contain contract data
    model_config = ConfigDict(from_attributes=True)



def create_customer(customer_data: Customer) -> Customer:
    """Create a new customer in the database

    Args:
        customer_data (Customer): The customer data to create

    Returns:
        Customer: The created customer with database-populated fields
    """
    db_customer = CustomerModel(
        firstName=customer_data.firstName,
        lastName=customer_data.lastName,
        mobileNumber=customer_data.mobileNumber,
        email=customer_data.email,
        createdAt=datetime.utcnow(),
        updatedAt=datetime.utcnow()
    )
    DB_SESSION.add(db_customer)
    DB_SESSION.commit()
    DB_SESSION.refresh(db_customer)
    return db_customer


def get_all_customers() -> list[Customer]:
    """Retrieve all customers from the database

    Returns:
        list[Customer]: List of all customers in the database
    """
    customers = DB_SESSION.query(CustomerModel).all()
    return customers


def get_customer_by_id(customer_id: int) -> Optional[Customer]:
    """Retrieve a customer by their ID

    Args:
        customer_id (int): The ID of the customer to retrieve

    Returns:
        Optional[Customer]: The customer if found, None otherwise
    """
    customer = DB_SESSION.query(CustomerModel).filter(CustomerModel.id == customer_id).first()
    return customer


