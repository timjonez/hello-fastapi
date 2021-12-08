from fastapi import FastAPI, HTTPException
from db import database, Users
import uuid

app = FastAPI()

@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()

@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()


RequestUser = Users.get_pydantic(exclude={"id", "is_active", "pub_id"})
ResponseUser = Users.get_pydantic(exclude={"password": ...})

@app.post("/account/create/", response_model=ResponseUser)
async def create_user(user: RequestUser):
    user_dict = user.dict()
    email = user_dict.get("email")
    if not await Users.objects.get_or_none(email=email):
        user_dict['pub_id'] = uuid.uuid4()
        return await Users(**user_dict).save()
    raise HTTPException(status_code=400, detail="Email already registered")
    
