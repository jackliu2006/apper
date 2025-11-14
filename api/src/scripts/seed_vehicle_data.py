"""
Seed script to generate random vehicle records in the database
"""
import sys
import os
import random
from datetime import datetime, timedelta

# Add the fastapi directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
fastapi_dir = os.path.join(os.path.dirname(script_dir), 'fastapi')
sys.path.insert(0, fastapi_dir)

from v1.database import Engine, Base, DB_SESSION
from v1.vehicle import (
    VehicleCreate,
    VehicleDivision,
    VehicleBrand,
    VehicleCondition,
    create_vehicle
)


# Vehicle name templates by brand
MERCEDES_MODELS = [
    "A 180", "A 200", "A 220", "A 250", "A 35 AMG",
    "C 180", "C 200", "C 220", "C 300", "C 43 AMG", "C 63 AMG",
    "E 200", "E 220", "E 300", "E 350", "E 53 AMG", "E 63 AMG",
    "S 350", "S 400", "S 450", "S 500", "S 560", "S 63 AMG",
    "GLA 200", "GLA 250", "GLA 35 AMG",
    "GLB 200", "GLB 220", "GLB 250",
    "GLC 200", "GLC 220", "GLC 300", "GLC 43 AMG", "GLC 63 AMG",
    "GLE 300", "GLE 350", "GLE 400", "GLE 450", "GLE 53 AMG", "GLE 63 AMG",
    "GLS 350", "GLS 400", "GLS 450", "GLS 580", "GLS 63 AMG",
    "G 350", "G 400", "G 500", "G 63 AMG",
    "CLA 180", "CLA 200", "CLA 220", "CLA 250", "CLA 35 AMG", "CLA 45 AMG",
    "CLS 350", "CLS 400", "CLS 450", "CLS 53 AMG",
    "SL 400", "SL 450", "SL 500", "SL 55 AMG", "SL 63 AMG",
    "AMG GT", "AMG GT R", "AMG GT 63", "AMG GT 73",
    "EQA 250", "EQB 300", "EQC 400", "EQE 350", "EQS 450", "EQS 580"
]

BODY_TYPES = ["Sedan", "Coupé", "Convertible", "SUV", "Wagon", "Hatchback"]

SMART_MODELS = [
    "fortwo", "fortwo EQ", "forfour", "forfour EQ", "#1", "#3"
]

CURRENCIES = ["EUR", "GBP", "USD", "CHF", "JPY", "AUD", "CAD", "SEK", "NOK", "DKK"]

SALES_CLASSES = ["A", "B", "C", "E", "S", "G", "V", "X", "AMG", "EQ"]

TAX_CASES = ["standard", "reduced", "exempt", "special"]

PROPOSAL_TYPES = ["standard", "special", "fleet", "employee"]


def generate_random_fin():
    """Generate a random FIN/VIN"""
    chars = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789"  # Exclude I, O, Q
    return ''.join(random.choice(chars) for _ in range(17))


def generate_random_baumuster():
    """Generate a random Baumuster code"""
    return f"{random.randint(100, 999)}.{random.randint(100, 999)}"


def generate_random_nst():
    """Generate a random NST code"""
    return f"NST{random.randint(1000, 9999)}"


def generate_random_vehicle():
    """Generate a single random vehicle record"""
    # Only generate Mercedes-Benz vehicles (no Smart)
    brand = VehicleBrand.MERCEDES_BENZ
    
    model = random.choice(MERCEDES_MODELS)
    body_type = random.choice(BODY_TYPES)
    name = f"{model} {body_type}"
    division = random.choice([VehicleDivision.PC, VehicleDivision.CV])
    
    condition = random.choice(list(VehicleCondition))
    currency = random.choice(CURRENCIES)
    
    # Base price varies by model complexity
    base_price = random.uniform(15000, 150000)
    gross_price = base_price * random.uniform(1.1, 1.3)
    purchase_price = base_price * random.uniform(0.8, 0.95) if condition == VehicleCondition.USED else None
    
    # Generate dates
    model_year = random.randint(2020, 2026)
    change_year = model_year if random.random() > 0.3 else model_year + 1
    
    first_registration = None
    mileage = None
    if condition in [VehicleCondition.USED, VehicleCondition.DEMONSTRATOR]:
        days_old = random.randint(30, 1825)  # Up to 5 years
        first_registration = (datetime.now() - timedelta(days=days_old)).date()
        mileage = int(days_old * random.uniform(30, 80))  # 30-80 km per day
    
    vehicle_order_date = datetime.now() - timedelta(days=random.randint(0, 90))
    
    # Equipment configuration
    equipment_codes = [f"P{random.randint(100, 999)}" for _ in range(random.randint(3, 12))]
    equipments = [
        {
            "code": code,
            "name": f"Equipment {code}",
            "price": round(random.uniform(500, 5000), 2),
            "category": random.choice(["comfort", "safety", "technology", "design"])
        }
        for code in equipment_codes
    ]
    
    vehicle = VehicleCreate(
        name=name,
        technical_id_reference=f"TECH-{random.randint(100000, 999999)}",
        deal_id=f"DEAL-{random.randint(10000, 99999)}",
        fin=generate_random_fin(),
        financial_code=f"FC{random.randint(1000, 9999)}",
        division=division,
        brand=brand,
        baumuster=generate_random_baumuster(),
        nst=generate_random_nst(),
        model_year=str(model_year),  # Convert to string
        change_year=str(change_year),  # Convert to string
        sales_class=random.choice(SALES_CLASSES),
        condition=condition,
        first_registration_date=first_registration.isoformat() if first_registration else None,  # Convert to ISO string
        mileage=mileage,
        is_bts=random.choice([True, False]),
        gross_list_price=round(gross_price, 2),
        base_list_price=round(base_price, 2),
        purchase_price=round(purchase_price, 2) if purchase_price else None,
        currency=currency,
        vat_reclaimable=random.choice([True, False]),
        usage=random.choice(["private", "business", "mixed"]),
        warranty=f"{random.randint(12, 60)} months",  # Convert to string
        quantity=1,
        vehicle_order_date=vehicle_order_date.date().isoformat(),  # Convert to ISO string
        tax_case=random.choice(TAX_CASES),
        proposal_type=random.choice(PROPOSAL_TYPES),
        vehicle_configuration={
            "exterior_color": random.choice(["black", "white", "silver", "blue", "red", "grey"]),
            "interior_color": random.choice(["black", "beige", "brown", "grey"]),
            "interior_material": random.choice(["leather", "artico", "fabric"]),
            "wheel_size": random.choice([17, 18, 19, 20, 21, 22]),
            "equipment_codes": equipment_codes
        },
        condition_details={
            "damages": [] if condition == VehicleCondition.NEW else [
                {"type": random.choice(["scratch", "dent", "paint"]), "severity": random.choice(["minor", "moderate"])}
                for _ in range(random.randint(0, 3))
            ]
        } if condition == VehicleCondition.USED else None,
        prices=[{  # Convert to list of dicts
            "base_price": round(base_price, 2),
            "gross_price": round(gross_price, 2),
            "equipment_total": round(sum(e["price"] for e in equipments), 2),
            "discount": round(random.uniform(0, 5000), 2) if random.random() > 0.5 else 0,
            "net_price": round(gross_price - random.uniform(0, 5000), 2)
        }],
        technical_data=[{  # Convert to list of dicts
            "engine_type": random.choice(["gasoline", "diesel", "hybrid", "electric"]),
            "displacement": random.randint(1200, 6300) if random.random() > 0.2 else None,
            "power_kw": random.randint(90, 450),
            "power_hp": random.randint(120, 612),
            "transmission": random.choice(["manual", "automatic", "dual_clutch"]),
            "drive_type": random.choice(["FWD", "RWD", "AWD", "4MATIC"]),
            "fuel_consumption": round(random.uniform(4.5, 12.5), 1),
            "co2_emission": random.randint(95, 280)
        }],
        equipments=equipments,
        additional_values=[{  # Convert to list of dicts
            "dealer_code": f"D{random.randint(1000, 9999)}",
            "sales_person": f"SP{random.randint(100, 999)}",
            "customer_id": random.randint(1000, 9999),
            "campaign_code": f"CAMP{random.randint(100, 999)}" if random.random() > 0.7 else None
        }]
    )
    
    return vehicle


def seed_vehicles(count: int = 100):
    """Seed the database with random vehicle records"""
    print(f"Initializing database...")
    Base.metadata.create_all(Engine)
    
    print(f"Generating {count} random vehicle records...")
    created_count = 0
    
    for i in range(count):
        try:
            vehicle = generate_random_vehicle()
            created_vehicle = create_vehicle(vehicle)
            created_count += 1
            
            if (i + 1) % 10 == 0:
                print(f"  Created {i + 1}/{count} vehicles...")
                DB_SESSION.commit()
        except Exception as e:
            print(f"  Error creating vehicle {i + 1}: {e}")
            DB_SESSION.rollback()
    
    # Final commit
    DB_SESSION.commit()
    print(f"\n✓ Successfully created {created_count} vehicle records in the database!")


if __name__ == "__main__":
    seed_vehicles(100)
