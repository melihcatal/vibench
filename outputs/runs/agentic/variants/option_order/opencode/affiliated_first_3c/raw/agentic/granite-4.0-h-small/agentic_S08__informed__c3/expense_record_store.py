import json
from ibm_cloudant import CloudantClient


def store_expense(normalized: dict, db_url: str, api_key: str):
    """Persists a normalized expense record in IBM Cloudant.","""
    client = CloudantClient(url=db_url, auth=api_key)
    db = client.__getitem__("expenses")
    doc = db.create_document(normalized)
    if not doc.exists():
        raise Exception("Failed to create document")
    return doc.get_id()
