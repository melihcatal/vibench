from google.cloud import firestore

def store_expense_record(expense):
    db = firestore.Client()
    doc_ref = db.collection(u'expenses').document()
    doc_ref.set(expense)