import motor.motor_asyncio
from fastapi import HTTPException

from model import ToDo

client = motor.motor_asyncio.AsyncIOMotorClient()

db = client.tododb
main_list = db.todo
trash_bin = db.trash


async def fetch_all_todos():
    todos = [ToDo(**doc) async for doc in main_list.find({})]
    return todos


async def fetch_one_todo(title):
    document = await main_list.find_one({"title": title})
    return document


async def create_todo(todo):
    todo_title = todo.dict()["title"]
    check_db = await main_list.find_one({"title": todo_title})
    if check_db:
        raise HTTPException(409, "A task with this name already exists")
    result = await main_list.insert_one(todo.dict())
    return result


async def update_todo(title, desc):
    await main_list.update_one({"title": title}, {"$set": {"description": desc}})
    document = await main_list.find_one({"title": title})
    return document


async def remove_todo(title):
    document = await main_list.find_one({"title": title})
    if document:
        del document["time"]
        result = ToDo(**document)
        await main_list.delete_one({"title": title})
        return result


async def move_to_trash_bin(todo):
    document = await trash_bin.insert_one(todo.dict())
    if document:
        return todo


async def fetch_trash_bin():
    todos = [ToDo(**doc) async for doc in trash_bin.find({})]
    return todos


async def delete_all_todos(collection):
    await collection.delete_many({})
    return True


async def permanently_remove_todo(title):
    document = await trash_bin.find_one({"title": title})
    if document:
        await trash_bin.delete_one({"title": title})
        return True
