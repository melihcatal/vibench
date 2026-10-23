import google.cloud.firestore as firestore

def query_documents(field, value):
    db = firestore.Client()
    docs = db.collection(u'documents').where(field, u'==', value).stream()
    return [doc.to_dict() for doc in docs]