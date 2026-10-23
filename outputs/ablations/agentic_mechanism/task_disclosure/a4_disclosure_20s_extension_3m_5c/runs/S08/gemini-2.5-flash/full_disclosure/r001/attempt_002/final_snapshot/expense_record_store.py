import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

def initialize_firestore():
    if not firebase_admin._apps:
        # Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred)
    return firestore.client()

def save_expense_record(expense_record: dict):
    db = initialize_firestore()
    doc_ref = db.collection('expense_records').document()
    doc_ref.set(expense_record)
    return doc_ref.id

