
import os
import pymongo
from datetime import datetime
from messaging_models import ProcessingResult

def store_audit_record(result: ProcessingResult):
    """
    Persists a processed message record to MongoDB Atlas for auditing.

    Args:
        result: A ProcessingResult object containing the outcome of message processing.
    """
    mongo_uri = os.environ.get("MONGO_ATLAS_URI")
    if not mongo_uri:
        raise ValueError("MONGO_ATLAS_URI environment variable is not set.")

    try:
        # The provider is identified by the pymongo SDK and the Atlas connection string format
        client = pymongo.MongoClient(mongo_uri)
        db = client.get_database("message_audit_db") # Or get from URI
        collection = db["processed_messages"]

        record = result.to_dict()
        record["processed_at"] = datetime.utcnow()

        insert_result = collection.insert_one(record)
        record_id = str(insert_result.inserted_id)
        
        print(f"Successfully stored audit record with ID: {record_id}")
        result.audit_record_id = record_id
        return result

    except pymongo.errors.ConnectionFailure as e:
        print(f"Could not connect to MongoDB Atlas: {e}")
        result.status = "FAILURE"
        result.error_message = "Failed to store audit record (Connection Error)"
        return result
    except Exception as e:
        print(f"An error occurred while storing audit record: {e}")
        result.status = "FAILURE"
        result.error_message = f"Failed to store audit record: {e}"
        return result

if __name__ == '__main__':
    # Example Usage:
    # Set the following environment variable before running:
    # export MONGO_ATLAS_URI="mongodb+srv://<user>:<password>@<cluster-url>/<db_name>?retryWrites=true&w=majority"
    
    # from uuid import uuid4
    # # Create a sample processing result
    # sample_result = ProcessingResult(
    #     original_event_id=str(uuid4()),
    #     status="SUCCESS",
    #     summary="Deployment next Tuesday.",
    #     safety_check={"TOXICITY": 0.1},
    #     translation="Bonjour le monde!",
    # )

    # # Store it in MongoDB Atlas
    # store_audit_record(sample_result)
    pass
