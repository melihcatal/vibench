import os
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

def persist_processed_message(record: dict):
    """
    Persists a processed message record for later lookup in MongoDB Atlas.
    """
    mongo_uri = os.getenv("MONGODB_ATLAS_URI")
    if not mongo_uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable is not set.")

    db_name = os.getenv("MONGO_DB_NAME", "audit_db")
    collection_name = os.getenv("MONGO_COLLECTION_NAME", "processed_messages")

    try:
        client = MongoClient(mongo_uri)
        client.admin.command('ismaster')
        
        db = client[db_name]
        collection = db[collection_name]
        
        record_to_insert = record.copy()
        record_to_insert['processed_at'] = datetime.utcnow()
        
        result = collection.insert_one(record_to_insert)
        print(f"Successfully inserted record with ID: {result.inserted_id}")
        return result.inserted_id

    except ConnectionFailure as e:
        print(f"Could not connect to MongoDB Atlas: {e}")
        return None
    except OperationFailure as e:
        print(f"An error occurred during MongoDB operation: {e}")
        return None
    finally:
        if 'client' in locals() and client:
            client.close()
