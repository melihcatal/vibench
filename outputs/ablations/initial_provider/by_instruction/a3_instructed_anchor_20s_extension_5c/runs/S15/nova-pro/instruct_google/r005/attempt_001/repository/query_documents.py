from google.cloud import firestore

def query_documents(field, value):
    db = firestore.Client()
    docs = db.collection(u'documents').where(field, '==', value).stream()
    results = [doc.to_dict() for doc in docs]
    print(f'Documents with {field} == {value} fetched successfully: {results}')