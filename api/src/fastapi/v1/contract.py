from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean, Numeric
from sqlalchemy.orm import relationship
from .database import Base, DB_SESSION


class ContractModel(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    contractNumber = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)
    startDate = Column(DateTime, nullable=False)
    endDate = Column(DateTime, nullable=True)
    value = Column(Numeric(10, 2), nullable=False)
    isActive = Column(Boolean, default=True)
    customerId = Column(Integer, ForeignKey("customers.id"), nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow)


class Contract(BaseModel):
    """Contract represents a business agreement with a customer"""
    id: int
    contractNumber: str
    description: Optional[str] = None
    startDate: datetime
    endDate: Optional[datetime] = None
    value: float
    isActive: bool = True
    customerId: int
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


def create_contract(contract_data: Contract) -> Contract:
    """Create a new contract in the database
    
    Args:
        contract_data (Contract): The contract data to create
        
    Returns:
        Contract: The created contract with database-populated fields
    """
    db_contract = ContractModel(
        contractNumber=contract_data.contractNumber,
        description=contract_data.description,
        startDate=contract_data.startDate,
        endDate=contract_data.endDate,
        value=contract_data.value,
        isActive=contract_data.isActive,
        customerId=contract_data.customerId,
        createdAt=datetime.utcnow(),
        updatedAt=datetime.utcnow()
    )
    DB_SESSION.add(db_contract)
    DB_SESSION.commit()
    DB_SESSION.refresh(db_contract)
    return Contract.model_validate(db_contract)


def get_all_contracts() -> List[Contract]:
    """Retrieve all contracts from the database
    
    Returns:
        List[Contract]: List of all contracts in the database
    """
    contracts = DB_SESSION.query(ContractModel).all()
    return [Contract.model_validate(contract) for contract in contracts]


def get_contract_by_id(contract_id: int) -> Optional[Contract]:
    """Retrieve a contract by its ID
    
    Args:
        contract_id (int): The ID of the contract to retrieve
        
    Returns:
        Optional[Contract]: The contract if found, None otherwise
    """
    contract = DB_SESSION.query(ContractModel).filter(ContractModel.id == contract_id).first()
    return Contract.model_validate(contract) if contract else None


def get_contracts_by_customer(customer_id: int) -> List[Contract]:
    """Retrieve all contracts for a specific customer
    
    Args:
        customer_id (int): The ID of the customer
        
    Returns:
        List[Contract]: List of all contracts for the customer
    """
    contracts = DB_SESSION.query(ContractModel).filter(ContractModel.customerId == customer_id).all()
    return [Contract.model_validate(contract) for contract in contracts]