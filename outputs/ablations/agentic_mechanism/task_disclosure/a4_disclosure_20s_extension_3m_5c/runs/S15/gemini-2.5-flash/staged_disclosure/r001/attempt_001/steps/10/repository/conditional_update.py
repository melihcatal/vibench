
import os
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# Replace with your MongoDB Atlas connection string
# It's recommended to store this in environment variables for security
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://<username>:<password>@<cluster-url>/test?retryWrites=true&w=majority")
DB_NAME = "mydatabase"
COLLECTION_NAME = "documents"

def conditional_update(document_id: str, new_content: str, expected_version: int) -> bool:
    """
    Applies a conditional update to a document in MongoDB.
    The update only proceeds if the document's current version matches the expected_version.
    """
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Attempt to update the document only if its _id and version match
        result = collection.update_one(
            {"_id": document_id, "version": expected_version},
            {"$set": {"content": new_content, "version": expected_version + 1}}
        )

        if result.matched_count == 1:
            print(f"Document {document_id} updated successfully. New version: {expected_version + 1}")
            return True
        else:
            print(f"Document {document_id} not updated. Version mismatch or document not found.")
            return False

    except DuplicateKeyError:
        print(f"Duplicate key error for document {document_id}. This should not happen with _id as primary key.")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        if 'client' in locals() and client:
            client.close()

if __name__ == "__main__":
    # Example Usage:
    # This example assumes you have a document with _id="doc1" and version=1
    # in your "mydatabase.documents" collection.
    # You would typically insert a document first:
    # collection.insert_one({"_id": "doc1", "content": "initial content", "version": 1})

    # To run this, replace <username>, <password>, and <cluster-url> with your MongoDB Atlas credentials
    # and ensure you have pymongo installed (`pip install pymongo`).

    doc_id = "doc1"
    
    # Simulate an initial document (if it doesn't exist)
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        if collection.find_one({"_id": doc_id}) is None:
            collection.insert_one({"_id": doc_id, "content": "initial content", "version": 1})
            print(f"Inserted initial document {doc_id} with version 1.")
        else:
            print(f"Document {doc_id} already exists.")
        client.close()
    except Exception as e:
        print(f"Error during initial document setup: {e}")

    # Attempt a successful update
    print("\n--- Attempting successful update ---")
    success = conditional_update(doc_id, "updated content v2", 1) # Expect version 1
    print(f"Update successful: {success}")

    # Attempt an update that should fail due to version mismatch
    print("\n--- Attempting failed update due to version mismatch ---")
    fail = conditional_update(doc_id, "this content should not be saved", 1) # Still expecting version 1, but it's now 2
    print(f"Update successful: {fail}")

    # Attempt another successful update with the correct current version
    print("\n--- Attempting another successful update ---")
    success_again = conditional_update(doc_id, "updated content v3", 2) # Expect version 2
    print(f"Update successful: {success_again}")
