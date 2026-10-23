import os
import uuid
import firebase_admin
from firebase_admin import credentials, firestore
from document_models import NormalizedExpense


def expense_record_store(expense: NormalizedExpense) -> str:
    if not firebase_admin._apps:
        cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    expense_id = expense.get("id") or str(uuid.uuid4())
    expense["id"] = expense_id
    db.collection("expenses").document(expense_id).set(expense)
    return expense_id
