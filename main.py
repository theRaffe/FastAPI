from fastapi import FastAPI
from pydantic import BaseModel
from routers import products, users, jwt_auth_users,users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

class Msg(BaseModel):
    msg: str

app.include_router(products.router)
app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return {"message": "Hello World. Welcome to FastAPI!"}


@app.get("/path")
async def demo_get():
    return {"message": "This is /path endpoint, use a post request to transform the text to uppercase"}


@app.post("/path")
async def demo_post(inp: Msg):
    return {"message": inp.msg.upper()}


@app.get("/path/{path_id}")
async def demo_get_path_id(path_id: int):
    return {"message": f"This is /path/{path_id} endpoint, use post request to retrieve result"}