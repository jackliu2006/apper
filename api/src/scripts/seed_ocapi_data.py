"""
Script to seed random OCAPI calculation data into the database
"""
import sys
import os
import random
from datetime import datetime, timedelta

# Add the fastapi directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
fastapi_dir = os.path.join(os.path.dirname(script_dir), 'fastapi')
sys.path.insert(0, fastapi_dir)

from v1.database import Engine, Base
from v1.ocapi import (
    OCAPICalculationModel,
    MarketCode,
    CustomerType,
    ProductType,
    SubProductType,
    VehicleDivision,
    VehicleBrand,
    VehicleCondition
)

# Sample vehicle data
VEHICLE_NAMES = [
    "C 180 Coupé",
    "E 200 Sedan",
    "S 500 Limousine",
    "GLC 300 SUV",
    "A 220 Hatchback",
    "CLA 250 Coupe",
    "GLE 450 SUV",
    "AMG GT 63 S",
    "Sprinter Van 314",
    "Vito Tourer 116"
]

BAUMUSTER_CODES = [
    "2053401", "2131401", "2231501", "2531401", "1771401",
    "1181401", "2921401", "1901401", "9061401", "6391401"
]

NST_CODES = ["999", "101", "202", "303", "404", "505"]

SALES_CLASSES = ["C-Class", "E-Class", "S-Class", "GLC", "A-Class", "CLA", "GLE", "AMG GT", "Sprinter", "Vito"]

CURRENCIES = ["EUR", "GBP", "USD", "CHF", "JPY", "AUD"]

USER_AGENTS = [
    "Salestablet/v1.2",
    "MBRetailApp/v2.3",
    "OnlineConfigurator/v3.1",
    "DealerPortal/v1.5",
    "MobileApp/v2.0"
]

ACCEPT_LANGUAGES = ["de-DE", "en-GB", "en-US", "fr-FR", "it-IT", "es-ES", "ja-JP", "zh-CN"]


def generate_random_calculation():
    """Generate a random OCAPI calculation record"""
    market = random.choice(list(MarketCode)).value
    customer_type = random.choice(list(CustomerType)).value
    product_type = random.choice(list(ProductType)).value
    sub_product_type = random.choice(list(SubProductType)).value
    
    vehicle_name = random.choice(VEHICLE_NAMES)
    vehicle_baumuster = random.choice(BAUMUSTER_CODES)
    vehicle_nst = random.choice(NST_CODES)
    vehicle_condition = random.choice(list(VehicleCondition)).value
    
    currency = random.choice(CURRENCIES)
    gross_list_price = round(random.uniform(25000, 120000), 2)
    calculated_rate = round(gross_list_price / random.randint(24, 60), 2)
    
    financial_code = f"fc_{market}_{random.randint(100000, 999999)}"
    opaque_token = f"opaque_{random.randint(1000000000, 9999999999)}"
    
    # Generate random timestamps within the last 30 days
    days_ago = random.randint(0, 30)
    created_at = datetime.utcnow() - timedelta(days=days_ago, hours=random.randint(0, 23))
    updated_at = created_at + timedelta(minutes=random.randint(0, 60))
    
    # Sample request payload
    request_payload = {
        "vehicle": {
            "name": vehicle_name,
            "vehicleConfiguration": {
                "baumuster": vehicle_baumuster,
                "nst": vehicle_nst,
                "salesDescription": vehicle_name,
                "division": random.choice([d.value for d in VehicleDivision]),
                "brand": random.choice([b.value for b in VehicleBrand])
            },
            "condition": {
                "condition": vehicle_condition
            },
            "prices": [
                {
                    "id": "grossListPrice",
                    "currency": currency,
                    "rawValue": gross_list_price,
                    "charges": []
                }
            ]
        },
        "customer": {
            "type": customer_type,
            "productType": product_type,
            "subProductType": sub_product_type
        },
        "input": [
            {"id": "term", "value": str(random.randint(24, 60))},
            {"id": "downpayment", "value": str(round(gross_list_price * random.uniform(0.1, 0.3), 2))}
        ]
    }
    
    # Sample response payload
    response_payload = {
        "output": {
            "financialCode": financial_code,
            "currency": currency,
            "widgetTitle": f"Mercedes-Benz Bank | Calculator [{market.upper()}]",
            "rate": f"{calculated_rate:.2f} {currency}",
            "rateData": calculated_rate,
            "messages": [],
            "financingProduct": {
                "id": str(random.randint(1, 5)),
                "label": f"{product_type.title()} - {sub_product_type.replace('_', ' ').title()}",
                "customerType": customer_type,
                "productType": product_type,
                "subProductType": sub_product_type,
                "isCampaign": random.choice([True, False])
            }
        },
        "code": 200,
        "type": "success",
        "message": "Calculation successful",
        "opaque": opaque_token
    }
    
    return OCAPICalculationModel(
        market=market,
        customer_type=customer_type,
        product_type=product_type,
        vehicle_name=vehicle_name,
        vehicle_baumuster=vehicle_baumuster,
        vehicle_nst=vehicle_nst,
        vehicle_condition=vehicle_condition,
        gross_list_price=gross_list_price,
        currency=currency,
        calculated_rate=calculated_rate,
        financial_code=financial_code,
        request_payload=request_payload,
        response_payload=response_payload,
        opaque_token=opaque_token,
        accept_language=random.choice(ACCEPT_LANGUAGES),
        user_agent=random.choice(USER_AGENTS),
        request_id=f"{random.randint(10000000, 99999999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(100000000000, 999999999999)}",
        created_at=created_at,
        updated_at=updated_at
    )


def main():
    """Main function to seed the database"""
    print("Creating database tables if they don't exist...")
    Base.metadata.create_all(bind=Engine)
    
    print("Generating 50 random OCAPI calculation records...")
    
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=Engine)
    session = Session()
    
    try:
        for i in range(50):
            calc = generate_random_calculation()
            session.add(calc)
            print(f"  [{i+1}/50] Created: {calc.vehicle_name} ({calc.market.upper()}) - {calc.currency} {calc.gross_list_price:.2f}")
        
        session.commit()
        print("\n✓ Successfully inserted 50 OCAPI calculation records into the database!")
        
        # Verify
        count = session.query(OCAPICalculationModel).count()
        print(f"✓ Total OCAPI calculations in database: {count}")
        
    except Exception as e:
        session.rollback()
        print(f"\n✗ Error occurred: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()
