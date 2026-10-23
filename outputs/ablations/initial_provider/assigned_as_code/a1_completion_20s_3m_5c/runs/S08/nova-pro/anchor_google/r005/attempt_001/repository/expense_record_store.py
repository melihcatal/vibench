from google.cloud import firestore

def store_expense_record(expense):
    client = firestore.Client()
    expense_ref = client.collection(u'expenses').document()
    expense_ref.set(expense)
    return expense_ref.id