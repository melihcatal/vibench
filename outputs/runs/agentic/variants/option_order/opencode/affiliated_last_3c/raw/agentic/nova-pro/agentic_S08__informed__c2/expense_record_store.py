from pymongo import MongoClient


def expense_record_store(expense):
    client = MongoClient("your_mongodb_uri")
    db = client["expense_db"]
    collection = db["expenses"]
    collection.insert_one(expense)
    return "Expense record stored successfully"
