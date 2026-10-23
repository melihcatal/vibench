from pymongo import MongoClient

def expense_record_store(expense_data):
    client = MongoClient(os.getenv('MONGODB_ATLAS_URI'))
    db = client.expense_db
    collection = db.expenses
    collection.insert_one(expense_data)