import os
import pymongo


def store_audit_event(event: dict):
    """
    Persists a federated login audit event to MongoDB Atlas.
    """
    connection_string = os.environ.get("MONGODB_ATLAS_URI")
    if not connection_string:
        raise ValueError("MONGODB_ATLAS_URI environment variable not set.")

    client = pymongo.MongoClient(connection_string)
    db = client.get_default_database()  # Or specify a DB name

    if db is None:
        # The database name should be part of the connection string.
        # If not, let's parse it or use a default.
        from urllib.parse import urlparse

        db_name = urlparse(connection_string).path[1:]
        if not db_name:
            db_name = "federated_logins"
        db = client[db_name]

    audit_collection = db["audit_events"]
    result = audit_collection.insert_one(event)
    return result.inserted_id
