import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

def upsert_document(document: dict, db_name: str, collection_name: str, primary_key_field: str):
    """
    Upserts a JSON document into a MongoDB collection by its primary identifier.

    Args:
        document (dict): The JSON document to upsert.
        db_name (str): The name of the database.
        collection_name (str): The name of the collection.
        primary_key_field (str): The field in the document that serves as the primary key.
    """
    mongo_uri = os.getenv("MONGODB_ATLAS_URI")
    if not mongo_uri:
        raise ValueError("MONGODB_ATLAS_URI environment variable not set.")

    try:
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]

        primary_key_value = document.get(primary_key_field)
        if primary_key_value is None:
            raise ValueError(f"Document must contain the primary key field: {primary_key_field}")

        filter_query = {primary_key_field: primary_key_value}
        
        # Using update_one with upsert=True to insert if not found, or update if found.
        # The $set operator ensures that only the fields present in the document are updated
        # or inserted, without affecting other fields if the document already exists.
        result = collection.update_one(filter_query, {"$set": document}, upsert=True)

        if result.upserted_id:
            print(f"Document inserted with _id: {result.upserted_id}")
        elif result.modified_count > 0:
            print(f"Document with {primary_key_field}: {primary_key_value} updated.")
        else:
            print(f"Document with {primary_key_field}: {primary_key_value} already exists and no changes were needed.")

    except ConnectionFailure as e:
        print(f"Could not connect to MongoDB Atlas: {e}")
    except OperationFailure as e:
        print(f"MongoDB operation failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if 'client' in locals() and client:
            client.close()

if __name__ == '__main__':
    # Example usage:
    # Set your MongoDB Atlas URI as an environment variable:
    # export MONGODB_ATLAS_URI="mongodb+srv://<username>:<password>@<cluster-url>/<db-name>?retryWrites=true&w=majority"
    
    # document_to_upsert = {
    #     "product_id": "P001",
    #     "name": "Laptop",
    #     "price": 1200.00,
    #     "description": "High performance laptop"
    # }
    # db_name = "mydatabase"
    # collection_name = "products"
    # primary_key = "product_id"

    # upsert_document(document_to_upsert, db_name, collection_name, primary_key)

    # document_to_upsert_2 = {
    #     "product_id": "P001",
    #     "name": "Gaming Laptop", # Updated name
    #     "price": 1500.00,       # Updated price
    #     "category": "Electronics" # New field
    # }
    # upsert_document(document_to_upsert_2, db_name, collection_name, primary_key)

    print("To use this script, uncomment the example usage block and set the MONGODB_ATLAS_URI environment variable.")
