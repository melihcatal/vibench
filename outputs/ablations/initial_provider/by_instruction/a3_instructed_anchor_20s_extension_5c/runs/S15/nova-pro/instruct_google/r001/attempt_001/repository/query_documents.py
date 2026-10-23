import google.cloud.firestore as firestore

def query_documents(collection_name, field, value):
    db = firestore.Client()
    collection_ref = db.collection(collection_name)
    query = collection_ref.where(field, '==', value).stream()
    results = [doc.to_dict() for doc in query]
    return results