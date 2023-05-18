from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from model import ToDo
from database import (
    creat_todo,
    fetch_all_todos,
    update_todo,
    fetch_one_todo,
    remove_todo,
    delete_all_todos,
)

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
    response = await fetch_all_todos()
    return response


@app.post("/api/todo/", response_model=ToDo)
async def post_todo(todo: ToDo):
    response = await creat_todo(todo.dict())
    if response:
        return response
    elif response == None:
        raise HTTPException(409, "A task with this name already exists")
    raise HTTPException(400, "Something went wrong")


@app.put("/api/todo/{title}/", response_model=ToDo)
async def put_todo(title: str, desc: str):
    response = await update_todo(title, desc)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with the title {title}")


@app.get("/api/todo/{title}", response_model=ToDo)
async def get_todo_by_id(title):
    response = await fetch_one_todo(title)
    if response:
        return response
    raise HTTPException(404, f"There is no todo with the title {title}")


@app.delete("/api/todo/{title}", response_model=ToDo)
async def delete_todo(title):
    response = await remove_todo(title)
    if response:
        return True
    raise HTTPException(404, f"There is no todo with the title {title}")


@app.delete("/api/todo/")
async def delete_all_todos_handler():
    response = await delete_all_todos()
    return response
