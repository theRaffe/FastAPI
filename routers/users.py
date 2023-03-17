from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["users"])


class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


user_list = [
    User(id=1, name="Brais", surname="Moure", url="https://moure.dev", age=35),
    User(id=2, name="Moure", surname="Dev",
         url="https://mouredev.com", age=35),
    User(id=3, name="Haakon", surname="Dahlberg",
         url="https://haakon.com", age=33),
]


@router.get("/usersJson")
async def usersJson():
    return [{"name": "Brais", "surname": "Moure", "url": "https://moure.dev", "age": 35},
            {"name": "Moure", "surname": "Dev",
                "url": "https://mouredev.com", "age": 35},
            {"name": "Haakon", "surname": "Dahlberg", "url": "https://haakon.com", "age": 33}]


@router.get("/users")
async def users():
    return user_list


@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)


@router.get("/userquery/")
async def user(id: int):
    return search_user(id)


@router.post("/user/", response_model=User, status_code=201)
async def add_user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="User id already exists")

    user_list.append(user)
    return user


@router.put("/user/")
async def update_user(user: User):
    found = False
    for index, saved_user in enumerate(user_list):
        if saved_user.id == user.id:
            user_list[index] = user
            found = True

    if not found:
        return {"error": "User not found"}
    return user


@router.delete("/user/")
async def delete_user(id: int):
    found_user = search_user(id)
    if type(found_user) == User:
        user_list.remove(found_user)
        return found_user

    return {"error": "Id not found, user couldn't be removed"}


def search_user(id: int):
    users = list(filter(lambda user: user.id == id, user_list))
    if len(users) > 0:
        return users[0]

    return {"error": "User not found!"}
