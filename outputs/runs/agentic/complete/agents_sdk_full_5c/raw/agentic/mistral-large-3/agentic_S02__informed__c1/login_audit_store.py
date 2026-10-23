from google.cloud import firestore
import os
from typing import Dict
from datetime import datetime


def store_login_audit_record(record: Dict) -> str:
    client = firestore.Client()
    db = client.collection("federated_login_audit")
    record["timestamp"] = datetime.utcnow()
    doc_ref = db.add(record)
    return doc_ref[1].id