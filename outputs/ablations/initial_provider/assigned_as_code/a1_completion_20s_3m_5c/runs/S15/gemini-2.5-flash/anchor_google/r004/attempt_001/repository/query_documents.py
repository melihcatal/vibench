from database_client import get_firestore_client
from database_models import QueryCondition

def query_documents(collection_name, project_id, conditions: list[QueryCondition]):
    client = get_firestore_client(project_id)
    collection_ref = client.collection(collection_name)

    query = collection_ref
    for condition in conditions:
        query = query.where(condition.field, condition.operator, condition.value)
    
    results = []
    for doc in query.stream():
        results.append({"id": doc.id, "document": doc.to_dict()})
    return results
