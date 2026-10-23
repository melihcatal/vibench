import os
from pymongo import MongoClient
from pymongo.errors import PyMongoError

def upsert_document(document: dict, collection_name: str, primary_key: str = "_id"):
    """
    Upserts a JSON document into a MongoDB collection.

    Args:
        document (dict): The JSON document to upsert.
        collection_name (str): The name of the MongoDB collection.
        primary_key (str): The field to use as the primary identifier for upsertion.
                           Defaults to "_id".
    """
    # MongoDB Atlas connection string (replace with your actual connection string)
    # It's recommended to store this in an environment variable for production.
    MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/?retryWrites=true&w=majority")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "mydatabase") # Replace with your database name

    if "<username>" in MONGO_URI or "<password>" in MONGO_URI or "<cluster-name>" in MONGO_URI:
        print("WARNING: Please replace placeholder values in MONGO_URI or set the MONGO_URI environment variable.")
        return

    try:
        client = MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[collection_name]

        # Prepare the filter based on the primary key
        if primary_key not in document:
            print(f"Error: Primary key '{primary_key}' not found in the document.")
            return

        filter_query = {primary_key: document[primary_key]}

        # Perform the upsert operation
        result = collection.update_one(filter_query, {"$set": document}, upsert=True)

        if result.upserted_id is not None:
            print(f"Document upserted with _id: {result.upserted_id}")
        else:
            print(f"Document matched by {primary_key}: {document[primary_key]} and updated.")

    except PyMongoError as e:
        print(f"MongoDB Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if 'client' in locals() and client:
            client.close()

if __name__ == "__main__":
    # Example Usage:
    # Set your MONGO_URI and DATABASE_NAME environment variables
    # export MONGO_URI="mongodb+srv://your_username:your_password@your_cluster.mongodb.net/?retryWrites=true&w=majority"
    # export DATABASE_NAME="your_database_name"

    test_document_1 = {
        "_id": "doc123",
        "name": "Alice",
        "age": 30,
        "city": "New York"
    }

    test_document_2 = {
        "_id": "doc456",
        "name": "Bob",
        "email": "bob@example.com"
    }

    # Update document 1
    test_document_1_update = {
        "_id": "doc123",
        "name": "Alice Smith",
        "age": 31,
        "city": "London"
    }

    print("--- Upserting test_document_1 ---")
    upsert_document(test_document_1, "mycollection")

    print("\n--- Upserting test_document_2 ---")
    upsert_document(test_document_2, "mycollection")

    print("\n--- Updating test_document_1 ---")
    upsert_document(test_document_1_update, "mycollection")

    print("\n--- Upserting a document with a custom primary key ---")
    custom_key_doc = {
        "product_id": "prod789",
        "name": "Laptop",
        "price": 1200
    }
    upsert_document(custom_key_doc, "products", primary_key="product_id")

    # Example of a document missing the primary key
    print("\n--- Upserting a document missing the primary key ---")
    bad_doc = {
        "name": "Missing ID",
        "value": 100
    }
    upsert_document(bad_doc, "mycollection", primary_key="custom_id")
