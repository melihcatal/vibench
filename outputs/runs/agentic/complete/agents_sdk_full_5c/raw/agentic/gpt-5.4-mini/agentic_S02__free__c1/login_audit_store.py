from __future__ import annotations

import os
from typing import Any, Dict

from google.cloud import firestore

FIRESTORE_PROJECT_ENV = "GOOGLE_CLOUD_PROJECT"


def store_login_audit(record: Dict[str, Any], collection: str = "federated_login_audit") -> str:
    client = firestore.Client(project=os.environ.get(FIRESTORE_PROJECT_ENV))
    doc = client.collection(collection).document()
    doc.set(record)
    return doc.id
