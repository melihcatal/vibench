import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

def upsert_document(document: dict, database_name: str, collection_name: str):
    """
    Upserts a JSON document by its primary identifier (_id) into a MongoDB Atlas collection.

    Args:
        document (dict): The JSON document to upsert. Must contain an "_id" field.
        database_name (str): The name of the MongoDB database.
        collection_name (str): The name of the MongoDB collection.
    """
    if "_id" not in document:
        raise ValueError("Document must contain an '_id' field for upsert operation.")

    # MongoDB Atlas connection string from environment variable
    MONGO_URI = os.getenv("MONGO_ATLAS_URI")
    if not MONGO_URI:
        raise ValueError("MONGO_ATLAS_URI environment variable not set.")

    client = None
    try:
        # Establish connection to MongoDB Atlas
        client = MongoClient(MONGO_URI)
        db = client[database_name]
        collection = db[collection_name]

        # Upsert the document
        # If a document with the same _id exists, it will be updated; otherwise, a new document will be inserted.
        result = collection.update_one(
            {"_id": document["_id"]},
            {"$set": document},
            upsert=True
        )

        if result.upserted_id:
            print(f"Document with _id {result.upserted_id} inserted successfully.")
        elif result.modified_count > 0:
            print(f"Document with _id {document["_id"]} updated successfully.")
        else:
            print(f"No changes made to document with _id {document["_id"]}.")

    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
        raise
    except Exception as e:
        print(f"An error occurred during document upsert: {e}")
        raise
    finally:
        if client:
            client.close()

if __name__ == "__main__":
    # Example Usage:
    # Set your MongoDB Atlas URI as an environment variable
    # export MONGO_ATLAS_URI="mongodb+srv://<username>:<password>@<cluster-url>/<dbname>?retryWrites=true&w=majority"

    # Example document to upsert
    test_document_1 = {"_id": "doc123", "name": "Alice", "age": 30}
    test_document_2 = {"_id": "doc456", "name": "Bob", "city": "New York"}
    test_document_3 = {"_id": "doc123", "name": "Alicia", "age": 31, "status": "active"} # Update existing

    db_name = "mydatabase"
    coll_name = "mycollection"

    print("Attempting to upsert test_document_1...")
    upsert_document(test_document_1, db_name, coll_name)

    print("
Attempting to upsert test_document_2...")
    upsert_document(test_document_2, db_name, coll_name)

    print("
Attempting to upsert test_document_3 (update doc123)...")
    upsert_document(test_document_3, db_name, coll_name)
