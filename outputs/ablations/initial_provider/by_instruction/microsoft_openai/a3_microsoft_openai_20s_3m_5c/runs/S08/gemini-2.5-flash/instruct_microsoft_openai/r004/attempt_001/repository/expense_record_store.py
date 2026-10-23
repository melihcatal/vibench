import os
from google.cloud import firestore
from document_models import NormalizedExpense

def persist_expense_record(expense_record: NormalizedExpense) -> str:
    # Initialize Google Cloud Firestore client
    # The client automatically picks up credentials from the environment (e.g., GOOGLE_APPLICATION_CREDENTIALS)
    db = firestore.Client()

    # Reference to the collection where expense records will be stored
    collection_ref = db.collection("expense_records")

    try:
        # Convert the Pydantic model to a dictionary for Firestore. 
        # Pydantic's .dict() method handles nested models and types like datetime.date.
        expense_data = expense_record.dict()
        
        # Firestore doesn't directly support `datetime.date` objects, so convert to string
        if 'transaction_date' in expense_data and isinstance(expense_data['transaction_date'], date):
            expense_data['transaction_date'] = expense_data['transaction_date'].isoformat()

        # Add a new document to the collection
        doc_ref = collection_ref.add(expense_data)

        return doc_ref[1].id # doc_ref is a tuple (update_time, document_reference)

    except Exception as e:
        print(f"An error occurred during persisting expense record to Firestore: {e}")
        raise
