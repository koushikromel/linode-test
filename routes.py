from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
from models import *


testrouter = APIRouter()


@testrouter.get("/", response_description="List all devices", response_model=List[Test])
def list_all_device(request: Request):
    device = list(request.app.database["wta"].find(limit=100))
    print("device is ", device)
    return device


@testrouter.post(
    "/",
    response_description="Create a new device",
    status_code=status.HTTP_201_CREATED,
    response_model=Test,
)
def create_device(request: Request, device: Test = Body(...)):
    device = jsonable_encoder(device)
    new_device = request.app.database["wta"].insert_one(device)
    created_device = request.app.database["wta"].find_one(
        {"_id": new_device.inserted_id}
    )
    return created_device


@testrouter.get(
    "/{id}", response_description="Get a single device by id", response_model=Test
)
def find_device(id: int, request: Request):
    if (device := request.app.database["wta"].find_one({"_id": id})) is not None:
        return device
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Test with ID {id} not found"
    )


@testrouter.put("/{id}", response_description="Update a device", response_model=Test)
def update_device(id: int, request: Request, device: TestUpdate = Body(...)):
    device = {k: v for k, v in device.dict().items() if v is not None}
    if len(device) >= 1:
        print("inside if and length of device is ", len(device))
        print(f"Device is {device}")
        update_result = request.app.database["wta"].update_one(
            {"_id": id}, {"$set": device}
        )
        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Test with ID {id} not found",
            )
    if (
        existing_device := request.app.database["wta"].find_one({"_id": id})
    ) is not None:
        return existing_device
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Test with ID {id} not found"
    )


@testrouter.delete("/{id}", response_description="Delete a device")
def delete_device(id: int, request: Request, response: Response):
    delete_result = request.app.database["wta"].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Test with ID {id} not found"
    )
