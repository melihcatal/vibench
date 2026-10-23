from pymongo import MongoClient


def expense_record_store(record: dict):
    client = MongoClient(__import__("os").environ["MONGODB_ATLAS_URI"])
    db = client.get_default_database()
    return db.expenses.insert_one(record).inserted_id
