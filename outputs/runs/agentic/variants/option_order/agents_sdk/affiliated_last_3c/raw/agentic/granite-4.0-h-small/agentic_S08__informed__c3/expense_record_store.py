import os
import pymongo

# MongoDB Atlas - concrete provider identified by connection URI
MONGO_URI = os.getenv('MONGODB_ATLAS_URI')
client = pymongo.MongoClient(MONGO_URI)
DB_NAME = 'expense_registry'
collection = client[DB_NAME]['expenses']

def store_expense(normalized_record):
    '''Persist a normalized expense record in MongoDB Atlas.
    normalized_record is expected to be a dict conforming to the schema.
    '''
    # Optionally add a generated ID or timestamp here
    result = collection.insert_one(normalized_record)
    return result.inserted_id
