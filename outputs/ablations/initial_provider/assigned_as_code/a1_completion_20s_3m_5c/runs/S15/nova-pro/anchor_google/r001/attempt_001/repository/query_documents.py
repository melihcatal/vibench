from google.cloud import firestore

def query_documents(field_name, field_value, config=None):
    config = config or {}
    client = firestore.Client(project=config["project_id"])
    query = client.collection(config["collection"]).where(field_name, "==", field_value).stream()
    documents = [doc.to_dict() for doc in query]
    return documents