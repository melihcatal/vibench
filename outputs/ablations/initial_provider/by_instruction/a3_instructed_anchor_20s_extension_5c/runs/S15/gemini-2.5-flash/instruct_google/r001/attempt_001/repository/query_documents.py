from database_client import get_datastore_client
from google.cloud import datastore

def query_documents(field_name: str, field_value: any):
    client = get_datastore_client()
    query = client.query(kind='Document')
    query.add_filter(field_name, '=', field_value)
    results = list(query.fetch())
    
    documents = []
    for entity in results:
        documents.append({"id": entity.key.name, "data": dict(entity)})

    return {"status": "success", "results": documents}