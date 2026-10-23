from database_client import FirestoreClient
from database_models import Document, DocumentQueryRequest


def query_documents(request: DocumentQueryRequest):
    db = FirestoreClient.get_client()
    docs_ref = (
        db.collection("documents").where(request.field, "==", request.value).stream()
    )
    documents = [Document(**doc.to_dict()) for doc in docs_ref]
    return {"status": "success", "documents": documents}
