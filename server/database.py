import motor.motor_asyncio
from model import ToDo


client = motor.motor_asyncio.AsyncIOMotorClient()

db = client.tododb
collection = db.todo
trash_bin = db.trash


async def fetch_all_todos():
    todos = [ToDo(**doc) async for doc in collection.find({})]
    return todos


async def create_todo(todo):
    check_db = await collection.find_one({"title": todo["title"]})
    if check_db:
        return None
    else:
        result = await collection.insert_one(todo)
        return result


async def update_todo(title, desc):
    await collection.update_one({"title": title}, {"$set": {"description": desc}})
    document = await collection.find_one({"title": title})
    return document


async def fetch_one_todo(title):
    document = await collection.find_one({"title": title})
    return document


async def remove_todo(title):
    await collection.delete_one({"title": title})
    return True


async def remove_todo(title):
    document = await collection.find_one({"title": title})
    await collection.delete_one({"title": title})
    # del document["_id"]
    return document


async def move_to_trash(todo):
    document = await trash_bin.insert_one(todo)
    return document