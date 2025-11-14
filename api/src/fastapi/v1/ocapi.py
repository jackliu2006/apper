from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import Optional, List, Literal
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, JSON, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .database import Base, DB_SESSION


# -------------------------
# Enums
# -------------------------

class MarketCode(str, Enum):
    """ISO 3166-1 alpha-2 country codes for enabled markets"""
    AT = "at"
    AU = "au"
    BE = "be"
    CH = "ch"
    CZ = "cz"
    DE = "de"
    DK = "dk"
    ES = "es"
    FR = "fr"
    GB = "gb"
    HU = "hu"
    IN = "in"
    IT = "it"
    JP = "jp"
    KR = "kr"
    LU = "lu"
    MX = "mx"
    MY = "my"
    NL = "nl"
    NZ = "nz"
    PL = "pl"
    PT = "pt"
    RO = "ro"
    SE = "se"
    SG = "sg"
    SK = "sk"
    TH = "th"
    TR = "tr"
    TW = "tw"
    ZA = "za"


class CustomerType(str, Enum):
    """Type of customer"""
    PRIVATE = "private"
    BUSINESS = "business"


class ProductType(str, Enum):
    """Product type"""
    LEASING = "leasing"
    FINANCING = "financing"


class SubProductType(str, Enum):
    """Sub-product type"""
    FINANCING_STANDARD = "financing_standard"
    FINANCING_BALLOON = "financing_balloon"
    FINANCING_OPTION = "financing_option"
    LEASING_OPERATING = "leasing_operating"
    LEASING_OPERATING_OPTIONS = "leasing_operating_options"
    LEASING_FINANCE = "leasing_finance"
    LEASING_FINANCE_OPTIONS = "leasing_finance_options"
    LEASING_FINANCE_BALLOON = "leasing_finance_balloon"


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

class OCAPICalculationModel(Base):
    """Database model for OCAPI calculation requests and responses"""
    __tablename__ = "ocapi_calculations"

    id = Column(Integer, primary_key=True, index=True)
    market = Column(String(2), nullable=False, index=True)
    customer_type = Column(String(20), nullable=True)
    product_type = Column(String(20), nullable=True)
    vehicle_name = Column(String(255), nullable=True)
    vehicle_baumuster = Column(String(50), nullable=True)
    vehicle_nst = Column(String(50), nullable=True)
    vehicle_condition = Column(String(20), nullable=True)
    gross_list_price = Column(Float, nullable=True)
    currency = Column(String(3), nullable=True)
    calculated_rate = Column(Float, nullable=True)
    financial_code = Column(String(255), nullable=True)
    request_payload = Column(JSON, nullable=True)
    response_payload = Column(JSON, nullable=True)
    opaque_token = Column(Text, nullable=True)
    accept_language = Column(String(10), nullable=True)
    user_agent = Column(String(255), nullable=True)
    request_id = Column(String(36), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# -------------------------
# Pydantic Models for Request/Response
# -------------------------

class ChargeInfo(BaseModel):
    """Information about charges (taxes, fees, etc.)"""
    label: Optional[str] = None
    rawRate: Optional[float] = None
    rawAmount: Optional[float] = None
    exemptionAmount: Optional[float] = None
    type: Optional[Literal[
        "acquisitionTax", "automobileTax", "bpm", "carAssessmentFee", "co2Tax",
        "compulsoryInsurance", "costExpenses", "delivery", "deliveryFee", "ecv",
        "exciseTax", "frf", "garageFee", "garageHandlingFee", "inspectionFee",
        "inspectionHandlingFee", "ipt", "isv", "licensePlateFee", "maintenancePackageFee",
        "notarialFee", "nova", "otherNonTaxableFee", "ownershipClaimFee", "preparationFee",
        "recycleDeposit", "recyclingFee", "registrationTax", "roadTax", "stampDutyFee",
        "vat", "ved", "vrp", "warrantFee", "weightTax"
    ]] = None


class PriceInfo(BaseModel):
    """Price information with charges"""
    id: str = Field(..., description="ID of the price info")
    currency: str = Field(..., description="Currency code (e.g., EUR)")
    rawValue: float = Field(..., description="Raw value of the price")
    charges: List[ChargeInfo] = Field(default_factory=list)


class Equipment(BaseModel):
    """Vehicle equipment"""
    code: Optional[str] = None
    codeType: Optional[str] = None
    name: Optional[str] = None
    prices: Optional[List[PriceInfo]] = None


class VehicleConfiguration(BaseModel):
    """Vehicle configuration details"""
    division: Optional[VehicleDivision] = None
    brand: Optional[VehicleBrand] = None
    baumuster: Optional[str] = None
    nst: Optional[str] = None
    modelYear: Optional[str] = None
    changeYear: Optional[str] = None
    salesClass: Optional[str] = None
    salesDescription: Optional[str] = None
    equipments: List[Equipment] = Field(default_factory=list)


class VehicleConditionInfo(BaseModel):
    """Vehicle condition information"""
    firstRegistrationDate: Optional[str] = None
    condition: Optional[VehicleCondition] = None
    isBts: Optional[bool] = None


class Vehicle(BaseModel):
    """Vehicle information for calculation"""
    technicalIdReference: Optional[str] = None
    dealId: Optional[str] = None
    fin: Optional[str] = None
    vehicleConfiguration: Optional[VehicleConfiguration] = None
    condition: Optional[VehicleConditionInfo] = None
    name: Optional[str] = None
    prices: List[PriceInfo] = Field(default_factory=list)
    financialCode: Optional[str] = None


class Customer(BaseModel):
    """Customer information"""
    type: Optional[CustomerType] = None
    segmentId: Optional[str] = None
    fleetAccountNumber: Optional[str] = None
    productType: Optional[ProductType] = None
    subProductType: Optional[SubProductType] = None
    regionCode: Optional[str] = None


class FinancialParameter(BaseModel):
    """Financial input parameter"""
    id: str = Field(..., description="Parameter ID (e.g., 'term', 'downpayment')")
    value: str = Field(..., description="Parameter value")


class CalculationRequest(BaseModel):
    """Request model for OCAPI calculation"""
    vehicle: Vehicle = Field(..., description="Vehicle information")
    customer: Optional[Customer] = None
    input: List[FinancialParameter] = Field(default_factory=list, description="Financial parameters")
    opaque: Optional[str] = Field(None, description="Opaque token from previous response")


class SingleValue(BaseModel):
    """Single value with formatting information"""
    label: Optional[str] = None
    label2: Optional[str] = None
    teaserText: Optional[str] = None
    value: Optional[str] = None
    unitFormatted: Optional[str] = None
    unit: Optional[str] = None
    selected: Optional[bool] = None
    format: Optional[str] = None
    info: Optional[str] = None


class InputField(BaseModel):
    """Input field definition"""
    type: Literal["oneOfMany", "number", "outputText", "boolean", "text"]
    subtype: Optional[str] = None
    businessContext: Optional[str] = None
    label: Optional[str] = None
    id: Optional[str] = None
    values: List[SingleValue] = Field(default_factory=list)
    value: Optional[SingleValue] = None
    minValue: Optional[SingleValue] = None
    maxValue: Optional[SingleValue] = None
    step: Optional[float] = None
    unitFormatted: Optional[str] = None
    highlight: Optional[bool] = None
    message: Optional[str] = None
    info: Optional[str] = None
    editable: Optional[bool] = None


class InputContainer(BaseModel):
    """Container for input fields"""
    id: Optional[str] = None
    label: Optional[str] = None
    items: List[InputField] = Field(default_factory=list)
    childContainers: List['InputContainer'] = Field(default_factory=list)


class FinancingResultRow(BaseModel):
    """Row in financing result output"""
    id: Optional[str] = None
    disclaimer: Optional[str] = None
    highlight: Optional[bool] = None
    infoTextKey: Optional[str] = None
    label: Optional[str] = None
    value: Optional[str] = None
    subtype: Optional[str] = None
    businessValue: Optional[str] = None
    unitFormatted: Optional[str] = None
    unit: Optional[str] = None


class OutputContainer(BaseModel):
    """Container for output results"""
    id: Optional[str] = None
    label: Optional[str] = None
    items: List[FinancingResultRow] = Field(default_factory=list)
    childContainers: List['OutputContainer'] = Field(default_factory=list)


class Link(BaseModel):
    """Link definition"""
    label: Optional[str] = None
    url: Optional[str] = None
    id: Optional[str] = None
    classification: Optional[str] = None


class FinancingProduct(BaseModel):
    """Financing product information"""
    id: Optional[str] = None
    label: Optional[str] = None
    externalPosId: Optional[str] = None
    customerType: Optional[CustomerType] = None
    productType: Optional[ProductType] = None
    subProductType: Optional[SubProductType] = None
    isCampaign: Optional[bool] = None
    campaignLabel: Optional[str] = None
    campaignInfo: Optional[str] = None
    campaignId: Optional[str] = None


class Output(BaseModel):
    """Calculation output"""
    financialCode: Optional[str] = None
    currency: Optional[str] = None
    widgetTitle: Optional[str] = None
    rate: Optional[str] = None
    rateData: Optional[float] = None
    messages: List[str] = Field(default_factory=list)
    financingProduct: Optional[FinancingProduct] = None
    containers: List[OutputContainer] = Field(default_factory=list)
    links: List[Link] = Field(default_factory=list)


class CalculationResponse(BaseModel):
    """Response model for OCAPI calculation"""
    output: Optional[Output] = None
    input: Optional[InputContainer] = None
    tables: Optional[List] = None
    code: Optional[int] = None
    type: Optional[str] = None
    message: Optional[str] = None
    opaque: Optional[str] = None


class ErrorResponseBody(BaseModel):
    """Error response body"""
    status: int
    code: int
    message: str
    doc_url: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response wrapper"""
    error: ErrorResponseBody


class HealthDownstream(BaseModel):
    """Health status of downstream service"""
    proxy: Optional[str] = None
    statusCode: Optional[int] = None
    details: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    downstream: List[HealthDownstream] = Field(default_factory=list)


class OCAPICalculation(BaseModel):
    """Pydantic model for OCAPI calculation (for ORM interaction)"""
    id: int
    market: str
    customer_type: Optional[str] = None
    product_type: Optional[str] = None
    vehicle_name: Optional[str] = None
    vehicle_baumuster: Optional[str] = None
    vehicle_nst: Optional[str] = None
    vehicle_condition: Optional[str] = None
    gross_list_price: Optional[float] = None
    currency: Optional[str] = None
    calculated_rate: Optional[float] = None
    financial_code: Optional[str] = None
    request_payload: Optional[dict] = None
    response_payload: Optional[dict] = None
    opaque_token: Optional[str] = None
    accept_language: Optional[str] = None
    user_agent: Optional[str] = None
    request_id: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# -------------------------
# Service Functions (Mockup)
# -------------------------

def perform_calculation(
    market: MarketCode,
    calculation_request: CalculationRequest,
    accept_language: Optional[str] = None,
    user_agent: Optional[str] = None,
    request_id: Optional[str] = None
) -> CalculationResponse:
    """
    Perform a mock OCAPI calculation and store the request/response in database
    
    Args:
        market: ISO 3166-1 alpha-2 country code
        calculation_request: The calculation request data
        accept_language: Accept-Language header value
        user_agent: User-Agent header value
        request_id: X-Request-ID header value
    
    Returns:
        CalculationResponse: Mock calculation response
    """
    # Extract vehicle and customer info
    vehicle = calculation_request.vehicle
    customer = calculation_request.customer
    
    # Extract prices
    gross_price = None
    currency = "EUR"
    if vehicle.prices:
        for price in vehicle.prices:
            if price.id == "grossListPrice":
                gross_price = price.rawValue
                currency = price.currency
                break
    
    # Mock calculation: simple rate calculation (price / 36 months)
    mock_rate = (gross_price / 36) if gross_price else 500.0
    mock_financial_code = f"mock_{market.value}_{datetime.utcnow().timestamp()}"
    
    # Create mock response
    mock_output = Output(
        financialCode=mock_financial_code,
        currency=currency,
        widgetTitle=f"Mercedes-Benz Bank | Calculator [{market.value.upper()}]",
        rate=f"{mock_rate:.2f} {currency}",
        rateData=mock_rate,
        messages=[],
        financingProduct=FinancingProduct(
            id="1",
            label="Standard Financing",
            customerType=customer.type if customer else CustomerType.PRIVATE,
            productType=ProductType.FINANCING,
            subProductType=SubProductType.FINANCING_STANDARD,
            isCampaign=False
        ),
        containers=[
            OutputContainer(
                id="output",
                label="Calculation Result",
                items=[
                    FinancingResultRow(
                        id="monthlyRate",
                        label="Monthly Rate",
                        value=f"{mock_rate:.2f} {currency}",
                        businessValue=f"{mock_rate:.2f}",
                        subtype="currency",
                        unitFormatted=currency,
                        highlight=True
                    ),
                    FinancingResultRow(
                        id="term",
                        label="Term",
                        value="36 months",
                        businessValue="36",
                        subtype="number",
                        unitFormatted="months"
                    )
                ]
            )
        ],
        links=[
            Link(
                id="close",
                label="Close",
                url="#",
                classification="default"
            )
        ]
    )
    
    response = CalculationResponse(
        output=mock_output,
        code=200,
        type="success",
        message="Calculation successful (mock)",
        opaque=f"mock_opaque_{datetime.utcnow().timestamp()}"
    )
    
    # Store in database
    db_calc = OCAPICalculationModel(
        market=market.value,
        customer_type=customer.type.value if customer and customer.type else None,
        product_type=customer.productType.value if customer and customer.productType else None,
        vehicle_name=vehicle.name,
        vehicle_baumuster=vehicle.vehicleConfiguration.baumuster if vehicle.vehicleConfiguration else None,
        vehicle_nst=vehicle.vehicleConfiguration.nst if vehicle.vehicleConfiguration else None,
        vehicle_condition=vehicle.condition.condition.value if vehicle.condition and vehicle.condition.condition else None,
        gross_list_price=gross_price,
        currency=currency,
        calculated_rate=mock_rate,
        financial_code=mock_financial_code,
        request_payload=calculation_request.model_dump(),
        response_payload=response.model_dump(),
        opaque_token=response.opaque,
        accept_language=accept_language,
        user_agent=user_agent,
        request_id=request_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    DB_SESSION.add(db_calc)
    DB_SESSION.commit()
    DB_SESSION.refresh(db_calc)
    
    return response


def get_health_status() -> HealthResponse:
    """
    Get mock health status of OCAPI service
    
    Returns:
        HealthResponse: Mock health status
    """
    mock_markets = ["de", "fr", "gb", "at", "ch"]
    
    downstream_statuses = [
        HealthDownstream(
            proxy=f"ocapi-v3-{market}-prd",
            statusCode=200,
            details=None
        )
        for market in mock_markets
    ]
    
    return HealthResponse(
        status="up",
        downstream=downstream_statuses
    )


def get_all_calculations() -> List[OCAPICalculation]:
    """
    Retrieve all OCAPI calculations from the database
    
    Returns:
        List[OCAPICalculation]: List of all calculations
    """
    calculations = DB_SESSION.query(OCAPICalculationModel).all()
    return calculations


def get_calculation_by_id(calculation_id: int) -> Optional[OCAPICalculation]:
    """
    Retrieve an OCAPI calculation by ID
    
    Args:
        calculation_id: The ID of the calculation to retrieve
    
    Returns:
        Optional[OCAPICalculation]: The calculation if found, None otherwise
    """
    calculation = DB_SESSION.query(OCAPICalculationModel).filter(
        OCAPICalculationModel.id == calculation_id
    ).first()
    return calculation


def get_calculations_by_market(market: str) -> List[OCAPICalculation]:
    """
    Retrieve all calculations for a specific market
    
    Args:
        market: The market code (ISO 3166-1 alpha-2)
    
    Returns:
        List[OCAPICalculation]: List of calculations for the market
    """
    calculations = DB_SESSION.query(OCAPICalculationModel).filter(
        OCAPICalculationModel.market == market
    ).all()
    return calculations


def get_calculations_by_request_id(request_id: str) -> List[OCAPICalculation]:
    """
    Retrieve calculations by request ID
    
    Args:
        request_id: The X-Request-ID value
    
    Returns:
        List[OCAPICalculation]: List of calculations with matching request ID
    """
    calculations = DB_SESSION.query(OCAPICalculationModel).filter(
        OCAPICalculationModel.request_id == request_id
    ).all()
    return calculations
