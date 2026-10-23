from __future__ import annotations

from google.cloud import firestore
import os


def onboarding_summary(account_id: str) -> dict:
    client = firestore.Client(project=os.environ["GOOGLE_CLOUD_PROJECT"])
    doc = client.collection("onboarding_summaries").document(account_id).get()
    data = doc.to_dict() if doc.exists else {}
    return {"provider": "google_firestore", "account_id": account_id, "summary": data}
