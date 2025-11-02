from fastapi import APIRouter, status, HTTPException
from .customer import Customer, create_customer, get_all_customers, get_customer_by_id
from .address import Address, create_address, get_all_addresses, get_address_by_id, get_addresses_by_customer
from .contract import Contract, create_contract, get_all_contracts, get_contract_by_id, get_contracts_by_customer
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
    return get_addresses_by_customer(customer_id)

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