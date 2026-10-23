import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

def persist_login_audit_record(record):
    # MongoDB Atlas connection string should be set as an environment variable
    # MONGODB_ATLAS_URI
    # Example: "mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/?retryWrites=true&w=majority"
    
    mongo_uri = os.environ.get("MONGODB_ATLAS_URI")
    if not mongo_uri:
        return {"error": "MONGODB_ATLAS_URI environment variable not set."}

    try:
        client = MongoClient(mongo_uri)
        db = client.get_database("federated_login_audits")
        audit_collection = db.get_collection("login_records")
        
        # Insert the record
        result = audit_collection.insert_one(record)
        
        client.close()
        return {"status": "success", "inserted_id": str(result.inserted_id)}
    except ConnectionFailure as e:
        return {"error": f"MongoDB connection failed: {e}"}
    except OperationFailure as e:
        return {"error": f"MongoDB operation failed: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}
