import pymongo
from pymongo.errors import ConnectionFailure

# MongoDB connection details
MONGO_URI = "mongodb://localhost:27017/"  # Replace with your MongoDB URI if different
DATABASE_NAME = "mydatabase"
COLLECTION_NAME = "mycollection"

def conditional_update(document_id: str, current_version: int, new_value: str):
    """
    Applies a conditional update to a document in MongoDB.
    The update only proceeds if the document's version matches current_version.
    """
    try:
        client = pymongo.MongoClient(MONGO_URI)
        db = client[DATABASE_NAME]
        collection = db[COLLECTION_NAME]

        # Ensure the document exists for demonstration purposes
        # In a real application, you might handle the case where the document doesn't exist differently
        collection.update_one(
            {"_id": document_id},
            {"$setOnInsert": {"version": 0, "data": "initial_data"}},
            upsert=True
        )

        # Conditional update: only update if the 'version' field matches current_version
        result = collection.update_one(
            {"_id": document_id, "version": current_version},
            {"$set": {"data": new_value, "version": current_version + 1}}
        )

        if result.matched_count == 1:
            if result.modified_count == 1:
                print(f"Document {document_id} updated successfully. New version: {current_version + 1}")
            else:
                print(f"Document {document_id} matched but was not modified (perhaps new_value was same as existing).")
        else:
            print(f"Document {document_id} not updated. Either not found or version mismatch. Expected version: {current_version}")

        client.close()
    except ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Example usage:
    doc_id = "my_unique_document"

    print("Attempting initial update (version 0 to 1)...")
    conditional_update(doc_id, 0, "first_update_data")

    print("
Attempting update with correct version (version 1 to 2)...")
    conditional_update(doc_id, 1, "second_update_data")

    print("
Attempting update with incorrect version (should fail)...")
    conditional_update(doc_id, 1, "failed_update_data")

    print("
Attempting update with correct version again (version 2 to 3)...")
    conditional_update(doc_id, 2, "third_update_data")
