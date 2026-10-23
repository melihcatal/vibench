import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def query_documents(field_name: str, field_value: str, collection_name: str):
    """
    Queries documents by a field value from a MongoDB Atlas collection.

    Args:
        field_name: The name of the field to query.
        field_value: The value of the field to match.
        collection_name: The name of the collection to query.
    """
    mongodb_uri = os.environ.get("MONGODB_URI")
    database_name = os.environ.get("MONGODB_DATABASE_NAME")

    if not mongodb_uri or not database_name:
        raise ValueError("MONGODB_URI and MONGODB_DATABASE_NAME environment variables must be set.")

    try:
        client = MongoClient(mongodb_uri)
        client.admin.command('ping') # Test connection
        db = client[database_name]
        collection = db[collection_name]
        
        query = {field_name: field_value}
        documents = list(collection.find(query))
        
        client.close()
        return documents
    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
