"""
expense_record_store.py

Persists normalized expense records in Google Cloud Firestore.
"""

import os
from typing import Dict, Any, Optional
from google.cloud import firestore
from document_models import Expense

def store_expense_record(expense: Expense, collection_name: str = "expenses") -> Optional[str]:
    """
    Persists a normalized Expense object into a Google Cloud Firestore collection.

    Args:
        expense: The Expense object to store.
        collection_name: The name of the Firestore collection to store the expense in.

    Returns:
        The ID of the created document, or None if the operation fails.
    """
    try:
        # GOOGLE_APPLICATION_CREDENTIALS environment variable must be set
        # to a service account key JSON file path.
        db = firestore.Client()

        doc_ref = db.collection(collection_name).document()
        doc_ref.set(expense.to_dict())

        return doc_ref.id
    except Exception as e:
        print(f"Error storing expense record in Firestore: {e}")
        return None

def get_expense_record(document_id: str, collection_name: str = "expenses") -> Optional[Dict[str, Any]]:
    """
    Retrieves an expense record from Firestore by its document ID.

    Args:
        document_id: The ID of the document to retrieve.
        collection_name: The name of the Firestore collection.

    Returns:
        A dictionary representing the expense record, or None if not found or an error occurs.
    """
    try:
        db = firestore.Client()
        doc_ref = db.collection(collection_name).document(document_id)
        doc = doc_ref.get()

        if doc.exists:
            return doc.to_dict()
        else:
            print(f"Document with ID {document_id} not found.")
            return None
    except Exception as e:
        print(f"Error retrieving expense record from Firestore: {e}")
        return None
