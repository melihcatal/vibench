import os
import firebase_admin
from firebase_admin import credentials, firestore
from document_models import NormalizedExpense


class ExpenseRecordStore:
    def __init__(self):
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        if not project_id:
            raise ValueError(
                "GOOGLE_CLOUD_PROJECT_ID environment variable not set for Firestore."
            )

        if not firebase_admin._apps:  # Initialize Firebase Admin SDK only once
            # For local development, ensure GOOGLE_APPLICATION_CREDENTIALS is set
            # or provide a path to a service account key file.
            # For deployment on Google Cloud, credentials are automatically inferred.
            cred = credentials.ApplicationDefault()
            firebase_admin.initialize_app(
                cred,
                {
                    "projectId": project_id,
                },
            )

        self.db = firestore.client()
        self.collection_name = "expense_records"

    def save_expense_record(self, expense: NormalizedExpense) -> str:
        # Convert Pydantic model to dictionary, excluding unset fields
        expense_data = expense.model_dump(exclude_unset=True)

        # Add a timestamp or unique ID if not present in the model
        doc_ref = self.db.collection(self.collection_name).add(expense_data)
        return doc_ref[1].id  # doc_ref is a tuple (update_time, DocumentReference)

    def get_expense_record(self, record_id: str) -> Optional[NormalizedExpense]:
        doc_ref = self.db.collection(self.collection_name).document(record_id)
        doc = doc_ref.get()
        if doc.exists:
            return NormalizedExpense(**doc.to_dict())
        return None
