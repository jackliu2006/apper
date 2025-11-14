from fastapi import APIRouter, status, HTTPException, Header
from typing import Optional
from .customer import Customer, create_customer, get_all_customers, get_customer_by_id
from .address import Address, create_address, get_all_addresses, get_address_by_id, get_addresses_by_customer
from .contract import Contract, create_contract, get_all_contracts, get_contract_by_id, get_contracts_by_customer
from .vehicle import (
    Vehicle,
    VehicleCreate,
    VehicleBrand,
    VehicleCondition,
    create_vehicle,
    get_all_vehicles,
    get_vehicle_by_id,
    get_vehicles_by_fin,
    get_vehicles_by_baumuster,
    get_vehicles_by_condition,
    get_vehicles_by_brand,
    update_vehicle,
    delete_vehicle
)
from .ocapi import (
    MarketCode,
    CalculationRequest,
    CalculationResponse,
    HealthResponse,
    ErrorResponse,
    perform_calculation,
    get_health_status,
    get_all_calculations,
    get_calculation_by_id,
    get_calculations_by_market,
    get_calculations_by_request_id
)
from .database import Base, Engine

router = APIRouter(prefix="/v1")
Base.metadata.create_all(bind=Engine)


@router.get("/customers", operation_id="getCustomers", tags=["customers"])
async def get_customers():
    """Get all customers
    
    Returns:
        List[Customer]: List of all customers in the database
    """
    return get_all_customers()

@router.post("/customers", operation_id="createCustomer", tags=["customers"], status_code=status.HTTP_201_CREATED)
async def create_customer_endpoint(customer: Customer):
    """Create a new customer
    
    Args:
        customer (Customer): The customer data to create
        
    Returns:
        Customer: The created customer with database-populated fields
    """
    return create_customer(customer)

@router.get("/customers/{customer_id}", operation_id="getCustomerById", tags=["customers"])
async def get_customer_by_id_endpoint(customer_id: int):
    """Get a customer by their ID
    
    Args:
        customer_id (int): The ID of the customer to retrieve
        
    Returns:
        Customer: The requested customer
        
    Raises:
        HTTPException: 404 if customer not found
    """
    customer = get_customer_by_id(customer_id)
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {customer_id} not found"
        )
    return customer

@router.post("/addresses", operation_id="createAddress", tags=["addresses"], status_code=status.HTTP_201_CREATED)
async def create_address_endpoint(address: Address):
    """Create a new address
    
    Args:
        address (Address): The address data to create
        
    Returns:
        AddressRead: The created address with database-populated fields
    """
    return create_address(address)

@router.get("/addresses", operation_id="getAddresses", tags=["addresses"])
async def get_addresses():
    """Get all addresses
    
    Returns:
        List[Address]: List of all addresses in the database
    """
    return get_all_addresses()

@router.get("/addresses/{address_id}", operation_id="getAddressById", tags=["addresses"])
async def get_address_by_id_endpoint(address_id: int):
    """Get an address by its ID
    
    Args:
        address_id (int): The ID of the address to retrieve
        
    Returns:
        Address: The requested address
        
    Raises:
        HTTPException: 404 if address not found
    """
    address = get_address_by_id(address_id)
    if address is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Address with ID {address_id} not found"
        )
    return address

@router.get("/customers/{customer_id}/addresses", operation_id="getCustomerAddresses", tags=["addresses", "customers"])
async def get_customer_addresses(customer_id: int):
    """Get all addresses for a specific customer
    
    Args:
        customer_id (int): The ID of the customer
        
    Returns:
        List[Address]: List of all addresses for the customer
        
    Raises:
        HTTPException: 404 if customer not found
    """
    # First verify the customer exists
    customer = get_customer_by_id(customer_id)
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {customer_id} not found"
        )
    return get_contracts_by_customer(customer_id)


# -------------------------
# Vehicle Endpoints
# -------------------------

@router.post("/vehicles", operation_id="createVehicle", tags=["vehicles"], status_code=status.HTTP_201_CREATED)
async def create_vehicle_endpoint(vehicle: VehicleCreate):
    """Create a new vehicle
    
    Args:
        vehicle (VehicleCreate): The vehicle data to create
        
    Returns:
        Vehicle: The created vehicle with database-populated fields
    """
    return create_vehicle(vehicle)


@router.get("/vehicles", operation_id="getVehicles", tags=["vehicles"])
async def get_vehicles():
    """Get all vehicles
    
    Returns:
        List[Vehicle]: List of all vehicles in the database
    """
    return get_all_vehicles()


@router.get("/vehicles/{vehicle_id}", operation_id="getVehicleById", tags=["vehicles"])
async def get_vehicle_by_id_endpoint(vehicle_id: int):
    """Get a vehicle by its ID
    
    Args:
        vehicle_id (int): The ID of the vehicle to retrieve
        
    Returns:
        Vehicle: The requested vehicle
        
    Raises:
        HTTPException: 404 if vehicle not found
    """
    vehicle = get_vehicle_by_id(vehicle_id)
    if vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with ID {vehicle_id} not found"
        )
    return vehicle


@router.get("/vehicles/fin/{fin}", operation_id="getVehiclesByFin", tags=["vehicles"])
async def get_vehicles_by_fin_endpoint(fin: str):
    """Get vehicles by FIN/VIN
    
    Args:
        fin (str): The vehicle FIN/VIN to search for
        
    Returns:
        List[Vehicle]: List of vehicles with matching FIN
    """
    return get_vehicles_by_fin(fin)


@router.get("/vehicles/baumuster/{baumuster}", operation_id="getVehiclesByBaumuster", tags=["vehicles"])
async def get_vehicles_by_baumuster_endpoint(baumuster: str):
    """Get vehicles by Baumuster code
    
    Args:
        baumuster (str): The Baumuster code to search for
        
    Returns:
        List[Vehicle]: List of vehicles with matching Baumuster
    """
    return get_vehicles_by_baumuster(baumuster)


@router.get("/vehicles/condition/{condition}", operation_id="getVehiclesByCondition", tags=["vehicles"])
async def get_vehicles_by_condition_endpoint(condition: VehicleCondition):
    """Get vehicles by condition
    
    Args:
        condition (VehicleCondition): The vehicle condition (new, used, demonstrator)
        
    Returns:
        List[Vehicle]: List of vehicles with matching condition
    """
    return get_vehicles_by_condition(condition)


@router.get("/vehicles/brand/{brand}", operation_id="getVehiclesByBrand", tags=["vehicles"])
async def get_vehicles_by_brand_endpoint(brand: VehicleBrand):
    """Get vehicles by brand
    
    Args:
        brand (VehicleBrand): The vehicle brand
        
    Returns:
        List[Vehicle]: List of vehicles with matching brand
    """
    return get_vehicles_by_brand(brand)


@router.put("/vehicles/{vehicle_id}", operation_id="updateVehicle", tags=["vehicles"])
async def update_vehicle_endpoint(vehicle_id: int, vehicle: VehicleCreate):
    """Update an existing vehicle
    
    Args:
        vehicle_id (int): The ID of the vehicle to update
        vehicle (VehicleCreate): The updated vehicle data
        
    Returns:
        Vehicle: The updated vehicle
        
    Raises:
        HTTPException: 404 if vehicle not found
    """
    updated_vehicle = update_vehicle(vehicle_id, vehicle)
    if updated_vehicle is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with ID {vehicle_id} not found"
        )
    return updated_vehicle


@router.delete("/vehicles/{vehicle_id}", operation_id="deleteVehicle", tags=["vehicles"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_vehicle_endpoint(vehicle_id: int):
    """Delete a vehicle
    
    Args:
        vehicle_id (int): The ID of the vehicle to delete
        
    Raises:
        HTTPException: 404 if vehicle not found
    """
    deleted = delete_vehicle(vehicle_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehicle with ID {vehicle_id} not found"
        )


# -------------------------
# OCAPI Calculation Endpoints
# -------------------------

@router.post("/{market}/calculations", operation_id="calculations", tags=["calculations"], response_model=CalculationResponse)
async def calculate_financing(
    market: MarketCode,
    calculation_request: CalculationRequest,
    accept_language: Optional[str] = Header(None, alias="Accept-Language"),
    user_agent: Optional[str] = Header(None, alias="User-Agent"),
    x_ocapi_user_interaction: Optional[str] = Header(None, alias="X-OCAPI-User-Interaction"),
    x_request_id: Optional[str] = Header(None, alias="X-Request-ID")
):
    """Calculate a new financing quote
    
    Calculate a new financing quote and return all that is needed to render
    the input fields as well as the result.
    
    Args:
        market: ISO 3166-1 alpha-2 country code of the market
        calculation_request: Calculation context including vehicle, customer, and input parameters
        accept_language: Language preference (e.g., de-DE, en-GB)
        user_agent: User agent string
        x_ocapi_user_interaction: User interaction tracking
        x_request_id: Unique request identifier for tracing
        
    Returns:
        CalculationResponse: Calculation result with financial parameters and output
        
    Raises:
        HTTPException: 400 for invalid input, 403 for forbidden, 500 for server errors
    """
    try:
        result = perform_calculation(
            market=market,
            calculation_request=calculation_request,
            accept_language=accept_language,
            user_agent=user_agent,
            request_id=x_request_id
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server error: {str(e)}"
        )


@router.get("/health", operation_id="health", tags=["health"], response_model=HealthResponse)
async def health_check():
    """Check if the calculation service is available
    
    Can be used to monitor whether the service is available. However must not
    be called before each calculation request.
    
    Returns:
        HealthResponse: Service health status with downstream proxy information
    """
    return get_health_status()


# -------------------------
# OCAPI Calculation Management Endpoints (Additional)
# -------------------------

@router.get("/calculations", operation_id="getAllCalculations", tags=["calculations"])
async def get_all_calculations_endpoint():
    """Get all OCAPI calculations from the database
    
    Returns:
        List[OCAPICalculation]: List of all calculations
    """
    return get_all_calculations()


@router.get("/calculations/{calculation_id}", operation_id="getCalculationById", tags=["calculations"])
async def get_calculation_by_id_endpoint(calculation_id: int):
    """Get an OCAPI calculation by its ID
    
    Args:
        calculation_id: The ID of the calculation to retrieve
        
    Returns:
        OCAPICalculation: The requested calculation
        
    Raises:
        HTTPException: 404 if calculation not found
    """
    calculation = get_calculation_by_id(calculation_id)
    if calculation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Calculation with ID {calculation_id} not found"
        )
    return calculation


@router.get("/calculations/market/{market}", operation_id="getCalculationsByMarket", tags=["calculations"])
async def get_calculations_by_market_endpoint(market: str):
    """Get all calculations for a specific market
    
    Args:
        market: The market code (ISO 3166-1 alpha-2)
        
    Returns:
        List[OCAPICalculation]: List of calculations for the market
    """
    return get_calculations_by_market(market)


@router.get("/calculations/request/{request_id}", operation_id="getCalculationsByRequestId", tags=["calculations"])
async def get_calculations_by_request_id_endpoint(request_id: str):
    """Get calculations by request ID
    
    Args:
        request_id: The X-Request-ID value
        
    Returns:
        List[OCAPICalculation]: List of calculations with matching request ID
    """
    return get_calculations_by_request_id(request_id)

@router.post("/contracts", operation_id="createContract", tags=["contracts"], status_code=status.HTTP_201_CREATED)
async def create_contract_endpoint(contract: Contract):
    """Create a new contract
    
    Args:
        contract (Contract): The contract data to create
        
    Returns:
        Contract: The created contract with database-populated fields
    """
    return create_contract(contract)

@router.get("/contracts", operation_id="getContracts", tags=["contracts"])
async def get_contracts():
    """Get all contracts
    
    Returns:
        List[Contract]: List of all contracts in the database
    """
    return get_all_contracts()

@router.get("/contracts/{contract_id}", operation_id="getContractById", tags=["contracts"])
async def get_contract_by_id_endpoint(contract_id: int):
    """Get a contract by its ID
    
    Args:
        contract_id (int): The ID of the contract to retrieve
        
    Returns:
        Contract: The requested contract
        
    Raises:
        HTTPException: 404 if contract not found
    """
    contract = get_contract_by_id(contract_id)
    if contract is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Contract with ID {contract_id} not found"
        )
    return contract

@router.get("/customers/{customer_id}/contracts", operation_id="getCustomerContracts", tags=["contracts", "customers"])
async def get_customer_contracts(customer_id: int):
    """Get all contracts for a specific customer
    
    Args:
        customer_id (int): The ID of the customer
        
    Returns:
        List[Contract]: List of all contracts for the customer
        
    Raises:
        HTTPException: 404 if customer not found
    """
    # First verify the customer exists
    customer = get_customer_by_id(customer_id)
    if customer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Customer with ID {customer_id} not found"
        )
    return get_contracts_by_customer(customer_id)