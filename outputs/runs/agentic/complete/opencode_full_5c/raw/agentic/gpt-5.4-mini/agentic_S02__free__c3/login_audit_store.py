import os
from typing import Mapping

from google.cloud import firestore


def store_audit_record(record: Mapping[str, object]) -> str:
    client = firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))
    doc = client.collection(
        os.getenv("AUDIT_COLLECTION", "federated_login_audit")
    ).document()
    doc.set(dict(record))
    return doc.id
