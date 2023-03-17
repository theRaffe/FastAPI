from bson import ObjectId
from fastapi import APIRouter, HTTPException, status
from db.schemas.user import user_schema, users_schema
from db.models.user import User
from db.client import db_client

router = APIRouter(prefix="/userdb",
                   tags=["users"])

user_list = []


@router.get("/", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

@router.get("/") # Query
async def user(id: str):
    return search_user("_id", ObjectId(id))


@router.get("/{id}") # Path
async def user(id: str):
    return search_user("_id", ObjectId(id))


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def add_user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User id already exists")

    user_dict = dict(user)
    del user_dict["id"]
    id = db_client.users.insert_one(user_dict).inserted_id
    new_user = user_schema(db_client.users.find_one({"_id": id}))
    return User(**new_user)


@router.put("/", response_model=User)
async def update_user(user: User):
    user_dict = dict(user)
    del user_dict["_id"]
    try:
        db_client.users.find_one_and_replace({"_id": user.id}, user_dict)
    except:
        return {"error": "User not found"}

    return search_user("_id", ObjectId(user.id))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: str):
    found = db_client.users.find_one_and_delete({"_id": ObjectId(id)})
    if not found:
        return {"error": "Id not found, user couldn't be removed"}



def search_user(field: str, key: any):
    try:
        user_db = user_schema(db_client.users.find_one({field: key}))
        return User(**user_db)
    except:
        return {"error": "User not found!"}
