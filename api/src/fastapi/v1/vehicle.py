from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, List
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, JSON
from sqlalchemy.orm import relationship
from .database import Base, DB_SESSION
from enum import Enum


# -------------------------
# Enums
# -------------------------

class VehicleDivision(str, Enum):
    """Division of the vehicle"""
    PC = "pc"
    CV = "cv"
    VAN = "van"


class VehicleBrand(str, Enum):
    """Brand name of the vehicle"""
    MERCEDES_BENZ = "mercedes-benz"
    MERCEDES_AMG = "mercedes-amg"
    SMART = "smart"
    OTHER = "other"


class VehicleCondition(str, Enum):
    """Condition of the vehicle"""
    NEW = "new"
    USED = "used"
    DEMONSTRATOR = "demonstrator"


# -------------------------
# Database Models
# -------------------------

class VehicleModel(Base):
    """Database model for vehicles"""
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    
    # Basic vehicle information
    name = Column(String(255), nullable=False)
    technical_id_reference = Column(String(255), nullable=True)
    deal_id = Column(String(255), nullable=True, index=True)
    fin = Column(String(17), nullable=True, index=True)  # Vehicle Identification Number
    financial_code = Column(String(255), nullable=True)
    
    # Configuration details
    division = Column(String(20), nullable=True)
    brand = Column(String(50), nullable=True)
    baumuster = Column(String(50), nullable=True, index=True)
    nst = Column(String(50), nullable=True)
    model_year = Column(String(10), nullable=True)
    change_year = Column(String(10), nullable=True)
    sales_class = Column(String(100), nullable=True)
    sales_description = Column(Text, nullable=True)
    
    # Condition information
    condition = Column(String(20), nullable=True)
    first_registration_date = Column(String(10), nullable=True)  # ISO-8601 date
    mileage = Column(Float, nullable=True)
    mileage_unit = Column(String(10), nullable=True)
    is_bts = Column(Boolean, nullable=True)  # Build to stock
    
    # Pricing information
    gross_list_price = Column(Float, nullable=True)
    base_list_price = Column(Float, nullable=True)
    purchase_price = Column(Float, nullable=True)
    currency = Column(String(3), nullable=True)
    
    # Additional attributes
    vat_reclaimable = Column(Boolean, nullable=True)
    usage = Column(String(50), nullable=True)  # taxi, driving instructor, etc.
    warranty = Column(String(50), nullable=True)  # CPO, etc.
    quantity = Column(Integer, nullable=True, default=1)
    vehicle_order_date = Column(String(10), nullable=True)  # ISO-8601 date
    tax_case = Column(String(50), nullable=True)
    proposal_type = Column(String(20), nullable=True, default="initial")
    initial_proposal_date = Column(String(10), nullable=True)
    proposal_version = Column(Integer, nullable=True)
    
    # JSON fields for complex nested data
    vehicle_configuration = Column(JSON, nullable=True)  # Full configuration object
    condition_details = Column(JSON, nullable=True)  # Condition object with mileage
    prices = Column(JSON, nullable=True)  # Array of price info
    technical_data = Column(JSON, nullable=True)  # Array of technical data
    equipments = Column(JSON, nullable=True)  # Array of equipment
    additional_values = Column(JSON, nullable=True)  # Additional values
    additional_attributes = Column(JSON, nullable=True)  # Additional vehicle attributes
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# -------------------------
# Pydantic Models
# -------------------------

class VehicleBase(BaseModel):
    """Base vehicle model with common fields"""
    name: str = Field(..., description="Name of the vehicle model")
    technical_id_reference: Optional[str] = Field(None, description="Technical reference ID")
    deal_id: Optional[str] = Field(None, description="Deal identifier")
    fin: Optional[str] = Field(None, description="Vehicle FIN/VIN")
    financial_code: Optional[str] = Field(None, description="Financial code")
    
    # Configuration
    division: Optional[VehicleDivision] = None
    brand: Optional[VehicleBrand] = None
    baumuster: Optional[str] = Field(None, description="Baumuster number")
    nst: Optional[str] = Field(None, description="National sales type")
    model_year: Optional[str] = None
    change_year: Optional[str] = None
    sales_class: Optional[str] = Field(None, description="Sales class (e.g., E-Class)")
    sales_description: Optional[str] = None
    
    # Condition
    condition: Optional[VehicleCondition] = None
    first_registration_date: Optional[str] = Field(None, description="ISO-8601 date")
    mileage: Optional[float] = None
    mileage_unit: Optional[str] = Field(None, description="km, miles, etc.")
    is_bts: Optional[bool] = Field(None, description="Build to stock vehicle")
    
    # Pricing
    gross_list_price: Optional[float] = None
    base_list_price: Optional[float] = None
    purchase_price: Optional[float] = None
    currency: Optional[str] = Field(None, description="Currency code (e.g., EUR)")
    
    # Additional attributes
    vat_reclaimable: Optional[bool] = None
    usage: Optional[str] = Field(None, description="Usage type: taxi, driving instructor, etc.")
    warranty: Optional[str] = None
    quantity: Optional[int] = Field(1, description="Number of vehicles")
    vehicle_order_date: Optional[str] = Field(None, description="ISO-8601 date")
    tax_case: Optional[str] = None
    proposal_type: Optional[str] = Field("initial", description="initial, change, or followUp")
    initial_proposal_date: Optional[str] = Field(None, description="ISO-8601 date")
    proposal_version: Optional[int] = None
    
    # Complex nested data
    vehicle_configuration: Optional[dict] = None
    condition_details: Optional[dict] = None
    prices: Optional[List[dict]] = None
    technical_data: Optional[List[dict]] = None
    equipments: Optional[List[dict]] = None
    additional_values: Optional[List[dict]] = None
    additional_attributes: Optional[List[dict]] = None


class VehicleCreate(VehicleBase):
    """Model for creating a new vehicle"""
    pass


class Vehicle(VehicleBase):
    """Vehicle model with database-populated fields"""
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# -------------------------
# Service Functions
# -------------------------

def create_vehicle(vehicle_data: VehicleCreate) -> Vehicle:
    """Create a new vehicle in the database

    Args:
        vehicle_data (VehicleCreate): The vehicle data to create

    Returns:
        Vehicle: The created vehicle with database-populated fields
    """
    db_vehicle = VehicleModel(
        name=vehicle_data.name,
        technical_id_reference=vehicle_data.technical_id_reference,
        deal_id=vehicle_data.deal_id,
        fin=vehicle_data.fin,
        financial_code=vehicle_data.financial_code,
        division=vehicle_data.division.value if vehicle_data.division else None,
        brand=vehicle_data.brand.value if vehicle_data.brand else None,
        baumuster=vehicle_data.baumuster,
        nst=vehicle_data.nst,
        model_year=vehicle_data.model_year,
        change_year=vehicle_data.change_year,
        sales_class=vehicle_data.sales_class,
        sales_description=vehicle_data.sales_description,
        condition=vehicle_data.condition.value if vehicle_data.condition else None,
        first_registration_date=vehicle_data.first_registration_date,
        mileage=vehicle_data.mileage,
        mileage_unit=vehicle_data.mileage_unit,
        is_bts=vehicle_data.is_bts,
        gross_list_price=vehicle_data.gross_list_price,
        base_list_price=vehicle_data.base_list_price,
        purchase_price=vehicle_data.purchase_price,
        currency=vehicle_data.currency,
        vat_reclaimable=vehicle_data.vat_reclaimable,
        usage=vehicle_data.usage,
        warranty=vehicle_data.warranty,
        quantity=vehicle_data.quantity,
        vehicle_order_date=vehicle_data.vehicle_order_date,
        tax_case=vehicle_data.tax_case,
        proposal_type=vehicle_data.proposal_type,
        initial_proposal_date=vehicle_data.initial_proposal_date,
        proposal_version=vehicle_data.proposal_version,
        vehicle_configuration=vehicle_data.vehicle_configuration,
        condition_details=vehicle_data.condition_details,
        prices=vehicle_data.prices,
        technical_data=vehicle_data.technical_data,
        equipments=vehicle_data.equipments,
        additional_values=vehicle_data.additional_values,
        additional_attributes=vehicle_data.additional_attributes,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    DB_SESSION.add(db_vehicle)
    DB_SESSION.commit()
    DB_SESSION.refresh(db_vehicle)
    return db_vehicle


def get_all_vehicles() -> List[Vehicle]:
    """Retrieve all vehicles from the database

    Returns:
        List[Vehicle]: List of all vehicles in the database
    """
    vehicles = DB_SESSION.query(VehicleModel).all()
    return vehicles


def get_vehicle_by_id(vehicle_id: int) -> Optional[Vehicle]:
    """Retrieve a vehicle by its ID

    Args:
        vehicle_id (int): The ID of the vehicle to retrieve

    Returns:
        Optional[Vehicle]: The vehicle if found, None otherwise
    """
    vehicle = DB_SESSION.query(VehicleModel).filter(VehicleModel.id == vehicle_id).first()
    return vehicle


def get_vehicles_by_fin(fin: str) -> List[Vehicle]:
    """Retrieve vehicles by FIN/VIN

    Args:
        fin (str): The vehicle FIN/VIN to search for

    Returns:
        List[Vehicle]: List of vehicles with matching FIN
    """
    vehicles = DB_SESSION.query(VehicleModel).filter(VehicleModel.fin == fin).all()
    return vehicles


def get_vehicles_by_baumuster(baumuster: str) -> List[Vehicle]:
    """Retrieve vehicles by Baumuster code

    Args:
        baumuster (str): The Baumuster code to search for

    Returns:
        List[Vehicle]: List of vehicles with matching Baumuster
    """
    vehicles = DB_SESSION.query(VehicleModel).filter(VehicleModel.baumuster == baumuster).all()
    return vehicles


def get_vehicles_by_condition(condition: VehicleCondition) -> List[Vehicle]:
    """Retrieve vehicles by condition (new, used, demonstrator)

    Args:
        condition (VehicleCondition): The vehicle condition to filter by

    Returns:
        List[Vehicle]: List of vehicles with matching condition
    """
    vehicles = DB_SESSION.query(VehicleModel).filter(VehicleModel.condition == condition.value).all()
    return vehicles


def get_vehicles_by_brand(brand: VehicleBrand) -> List[Vehicle]:
    """Retrieve vehicles by brand

    Args:
        brand (VehicleBrand): The vehicle brand to filter by

    Returns:
        List[Vehicle]: List of vehicles with matching brand
    """
    vehicles = DB_SESSION.query(VehicleModel).filter(VehicleModel.brand == brand.value).all()
    return vehicles


def update_vehicle(vehicle_id: int, vehicle_data: VehicleCreate) -> Optional[Vehicle]:
    """Update an existing vehicle

    Args:
        vehicle_id (int): The ID of the vehicle to update
        vehicle_data (VehicleCreate): The updated vehicle data

    Returns:
        Optional[Vehicle]: The updated vehicle if found, None otherwise
    """
    db_vehicle = DB_SESSION.query(VehicleModel).filter(VehicleModel.id == vehicle_id).first()
    if db_vehicle is None:
        return None
    
    # Update fields
    for field, value in vehicle_data.model_dump(exclude_unset=True).items():
        if hasattr(db_vehicle, field):
            if field in ['division', 'brand', 'condition'] and value is not None:
                setattr(db_vehicle, field, value.value if isinstance(value, Enum) else value)
            else:
                setattr(db_vehicle, field, value)
    
    db_vehicle.updated_at = datetime.utcnow()
    DB_SESSION.commit()
    DB_SESSION.refresh(db_vehicle)
    return db_vehicle


def delete_vehicle(vehicle_id: int) -> bool:
    """Delete a vehicle from the database

    Args:
        vehicle_id (int): The ID of the vehicle to delete

    Returns:
        bool: True if deleted, False if not found
    """
    db_vehicle = DB_SESSION.query(VehicleModel).filter(VehicleModel.id == vehicle_id).first()
    if db_vehicle is None:
        return False
    
    DB_SESSION.delete(db_vehicle)
    DB_SESSION.commit()
    return True
