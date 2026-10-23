from document_client import get_firestore_client
from document_models import NormalizedExpense
from google.cloud import firestore


def persist_expense_record(expense: NormalizedExpense):
    db: firestore.Client = get_firestore_client()

    # Reference to the collection where expenses will be stored
    expenses_ref = db.collection("expenses")

    # Convert Pydantic model to a dictionary for Firestore
    expense_dict = expense.dict()

    # Add a new document to the "expenses" collection
    # Firestore automatically generates a document ID if not provided
    doc_ref = expenses_ref.add(expense_dict)

    return doc_ref[1].id  # Return the ID of the newly created document
