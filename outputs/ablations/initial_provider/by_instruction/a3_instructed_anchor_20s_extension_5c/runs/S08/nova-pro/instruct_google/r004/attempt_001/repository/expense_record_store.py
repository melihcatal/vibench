from google.cloud import firestore

def store_expense_record(expense_record):
    client = firestore.Client()
    collection_ref = client.collection('expenses')
    collection_ref.add(expense_record)