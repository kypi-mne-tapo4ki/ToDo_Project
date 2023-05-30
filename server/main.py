from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from model import ToDo
import database

app = FastAPI()


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/todo")
async def get_todo():
    response = await database.fetch_all_todos()
    return response


@app.post("/api/todo/", response_model=ToDo)
async def post_todo(todo: ToDo):
    response = await database.create_todo(todo.dict())
    if response:
        return response
    elif response == None:
        raise HTTPException(409, "A task with this name already exists")
    raise HTTPException(400, "Something went wrong")


@app.put("/api/todo/{title}/", response_model=ToDo)
async def put_todo(title: str, desc: str):
    response = await database.update_todo(title, desc)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with the title {title}")


@app.get("/api/todo/{title}", response_model=ToDo)
async def get_todo_by_id(title):
    response = await database.fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with the title {title}")


@app.delete("/api/todo/{title}", response_model=ToDo)
async def delete_todo(title):
    response = await database.remove_todo(title)
    if response:
        document = await database.move_to_trash(response)
        return document
    raise HTTPException(404, f"There is no todo with the title {title}")


@app.delete("/api/todo/")
async def delete_all_todos_handler():
    response = await database.delete_all_todos()
    return response
