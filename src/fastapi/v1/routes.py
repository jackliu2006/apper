from fastapi import APIRouter, status
from .application import Application, create_application, get_all_applications

router = APIRouter(prefix="/v1")

@router.get("/applications", operation_id="getApplications", tags=["applications"])
async def getAllApplications():
    return get_all_applications()

@router.post("/applications", operation_id="createApplication", tags=["applications"], status_code=status.HTTP_201_CREATED  )
async def createApplication(app: Application):
    return create_application(app)