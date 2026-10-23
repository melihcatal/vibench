import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

def upsert_document(document: dict, primary_id_field: str):
    """
    Upserts a JSON document into MongoDB Atlas by its primary identifier.

    Args:
        document (dict): The JSON document to upsert.
        primary_id_field (str): The field in the document that serves as the primary identifier.
    """
    mongodb_uri = os.getenv("MONGODB_URI")
    if not mongodb_uri:
        raise ValueError("MONGODB_URI environment variable not set.")

    client = None
    try:
        # MongoDB Atlas connection
        client = MongoClient(mongodb_uri)
        db = client.get_database("mydatabase")  # Replace with your database name
        collection = db.get_collection("mycollection")  # Replace with your collection name

        # Extract the primary identifier from the document
        primary_id = document.get(primary_id_field)
        if primary_id is None:
            raise ValueError(f"Document must contain the primary identifier field: {primary_id_field}")

        # Upsert the document
        # If a document with the _id exists, it updates it. Otherwise, it inserts a new one.
        result = collection.update_one(
            {primary_id_field: primary_id},
            {"$set": document},
            upsert=True
        )

        if result.upserted_id:
            print(f"Document inserted with _id: {result.upserted_id}")
        else:
            print(f"Document matched and updated for {primary_id_field}: {primary_id}")

    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
        raise
    except OperationFailure as e:
        print(f"MongoDB operation failed: {e}")
        raise
    except ValueError as e:
        print(f"Error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise
    finally:
        if client:
            client.close()

if __name__ == "__main__":
    # Example Usage:
    # Set your MongoDB Atlas URI as an environment variable before running:
    # export MONGODB_URI="mongodb+srv://<username>:<password>@<cluster-url>/<database-name>?retryWrites=true&w=majority"

    # Example document
    doc1 = {"_id": "doc123", "name": "Test Document 1", "value": 100}
    doc2 = {"_id": "doc123", "name": "Updated Document 1", "value": 150} # Same _id to test update
    doc3 = {"_id": "doc456", "name": "New Document 2", "value": 200}

    try:
        print("Upserting doc1...")
        upsert_document(doc1, "_id")
        print("\nUpserting doc2 (should update doc1)...")
        upsert_document(doc2, "_id")
        print("\nUpserting doc3...")
        upsert_document(doc3, "_id")
    except Exception as e:
        print(f"Failed to upsert documents: {e}")
