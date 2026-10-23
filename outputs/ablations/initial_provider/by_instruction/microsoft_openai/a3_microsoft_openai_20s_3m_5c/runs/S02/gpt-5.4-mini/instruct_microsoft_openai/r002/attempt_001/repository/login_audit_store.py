from pymongo import MongoClient


def store_login_audit(record: dict) -> str:
    client = MongoClient()
    collection = client["federated_login"]["audit_events"]
    result = collection.insert_one(record)
    return str(result.inserted_id)
