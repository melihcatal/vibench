import pymongo


def expense_record_store(expense_record):
    client = pymongo.MongoClient(os.environ["MONGODB_ATLAS_URI"])
    db = client["expense_db"]
    collection = db["expense_collection"]
    collection.insert_one(expense_record)
