"""
Script to delete all vehicles with 'smart' in the name from the database
"""
import sys
import os

# Add the fastapi directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
fastapi_dir = os.path.join(os.path.dirname(script_dir), 'fastapi')
sys.path.insert(0, fastapi_dir)

from v1.database import Engine, Base, DB_SESSION
from v1.vehicle import VehicleModel


def delete_smart_vehicles_by_name():
    """Delete all vehicles with 'smart' in the name from the database"""
    print(f"Connecting to database...")
    
    # Query for all vehicles with 'smart' in the name (case-insensitive)
    smart_vehicles = DB_SESSION.query(VehicleModel).filter(
        VehicleModel.name.ilike('%smart%')
    ).all()
    
    count = len(smart_vehicles)
    print(f"Found {count} vehicles with 'smart' in the name to delete...")
    
    if count > 0:
        # Show some examples
        print("\nExamples:")
        for vehicle in smart_vehicles[:5]:
            print(f"  - ID {vehicle.id}: {vehicle.name} (Brand: {vehicle.brand})")
        if count > 5:
            print(f"  ... and {count - 5} more")
        
        # Delete all vehicles with 'smart' in name
        DB_SESSION.query(VehicleModel).filter(
            VehicleModel.name.ilike('%smart%')
        ).delete(synchronize_session=False)
        
        DB_SESSION.commit()
        print(f"\n✓ Successfully deleted {count} vehicles with 'smart' in the name from the database!")
    else:
        print("No vehicles with 'smart' in the name found in the database.")


if __name__ == "__main__":
    delete_smart_vehicles_by_name()
