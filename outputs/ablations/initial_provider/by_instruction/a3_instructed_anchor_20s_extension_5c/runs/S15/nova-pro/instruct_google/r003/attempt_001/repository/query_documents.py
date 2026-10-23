from google.cloud import firestore

db = firestore.client()

def query_documents(field, value):
    docs = db.collection(u'documents').where(field, u'==', value).stream()
    return [doc.to_dict() for doc in docs]