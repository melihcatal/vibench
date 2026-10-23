import os
from google.cloud import firestore

db = firestore.client()

def query_documents(collection_name, field, value):
    docs = db.collection(collection_name).where(field, '==', value).stream()
    results = []
    for doc in docs:
        results.append(doc.to_dict())
    print(f'Queried documents in collection {collection_name} with {field} == {value}')
    return results