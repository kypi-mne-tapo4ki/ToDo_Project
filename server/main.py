from fastapi import FastAPI, HTTPException, status
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
    response = await database.create_todo(todo)
    if response:
        return todo
    elif response is None:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "A task with this name already exists"
        )
    raise HTTPException(
        status.HTTP_400_BAD_REQUEST,
        "Something went wrong"
    )


@app.put("/api/todo/{title}/", response_model=ToDo)
async def put_todo(title: str, desc: str):
    response = await database.update_todo(title, desc)
    if response:
        return response
    raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        f"There is no todo with the title '{title}'"
    )


@app.get("/api/todo/{title}", response_model=ToDo)
async def get_todo_by_title(title):
    response = await database.fetch_one_todo(title)
    if response:
        return ToDo(**response)
    raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        f"There is no todo with the title '{title}'"
    )


@app.get("/api/trash-bin")
async def get_trash_bin():
    response = await database.fetch_trash_bin()
    return response


@app.delete("/api/todo/{title}", response_model=ToDo)
async def delete_todo(title):
    response = await database.remove_todo(title)
    if response:
        document = await database.move_to_trash_bin(response)
        if document:
            return document
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Something went wrong"
        )
    raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        f"There is no todo with the title '{title}'"
    )


@app.delete("/api/todo/")
async def clear_todos_handler():
    response = await database.delete_all_todos(database.main_list)
    return response


@app.delete("/api/trash-bin/")
async def clear_trash_bin_handler():
    response = await database.delete_all_todos(database.trash_bin)
    return response


@app.delete("/api/trash-bin/{title}")
async def permanently_delete_todo(title):
    response = await database.permanently_remove_todo(title)
    if response:
        return response
    raise HTTPException(
        status.HTTP_404_NOT_FOUND,
        f"There is no todo with the title '{title}'"
    )
