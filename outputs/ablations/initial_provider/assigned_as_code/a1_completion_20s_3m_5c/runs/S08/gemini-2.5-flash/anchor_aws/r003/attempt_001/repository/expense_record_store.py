import os
from google.cloud import firestore # Provider-specific import
from document_models import NormalizedExpense

# Initialize Google Cloud Firestore client
# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
# or running in an environment with appropriate service account permissions.
db = firestore.Client()

def persist_expense_record(expense: NormalizedExpense) -> str:
    try:
        # Create a new document in the 'expenses' collection
        # Firestore automatically generates a document ID if not provided.
        doc_ref = db.collection("expenses").document()
        expense_dict = expense.dict()
        
        # Convert Pydantic models to dict, ensuring nested models are also dicts
        # and handling optional fields that might be None.
        
        # Clean up None values if Firestore doesn't handle them well or for cleaner storage
        def remove_none_values(d):
            if isinstance(d, dict):
                return {k: remove_none_values(v) for k, v in d.items() if v is not None}
            elif isinstance(d, list):
                return [remove_none_values(elem) for elem in d if elem is not None]
            else:
                return d
        
        cleaned_expense_dict = remove_none_values(expense_dict)
        
        doc_ref.set(cleaned_expense_dict)
        expense.transaction_id = doc_ref.id
        print(f"Expense record stored with ID: {doc_ref.id}")
        return doc_ref.id
    except Exception as e:
        print(f"Error persisting expense record to Firestore: {e}")
        return "Error storing record."
