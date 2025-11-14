"""
Script to delete all Smart brand vehicles from the database
"""
import sys
import os

# Add the fastapi directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
fastapi_dir = os.path.join(os.path.dirname(script_dir), 'fastapi')
sys.path.insert(0, fastapi_dir)

from v1.database import Engine, Base, DB_SESSION
from v1.vehicle import VehicleModel, VehicleBrand


def delete_smart_vehicles():
    """Delete all Smart brand vehicles from the database"""
    print(f"Connecting to database...")
    
    # Query for all Smart vehicles
    smart_vehicles = DB_SESSION.query(VehicleModel).filter(
        VehicleModel.brand == VehicleBrand.SMART.value
    ).all()
    
    count = len(smart_vehicles)
    print(f"Found {count} Smart vehicles to delete...")
    
    if count > 0:
        # Delete all Smart vehicles
        DB_SESSION.query(VehicleModel).filter(
            VehicleModel.brand == VehicleBrand.SMART.value
        ).delete()
        
        DB_SESSION.commit()
        print(f"✓ Successfully deleted {count} Smart vehicles from the database!")
    else:
        print("No Smart vehicles found in the database.")


if __name__ == "__main__":
    delete_smart_vehicles()
