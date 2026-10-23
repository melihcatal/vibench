from pymongo import MongoClient

MONGODB_ATLAS_URI = 'your_mongodb_atlas_uri'

def store_expense_record(record):
    client = MongoClient(MONGODB_ATLAS_URI)
    db = client.expense_db
    collection = db.expense_collection
    collection.insert_one(record)
    # Confirm record stored
    return 'Record stored successfully'