from database_client import get_cosmos_client
from database_models import Document

def upsert_document(document_id: str, content: dict, doc_type: str = "general"):
    container = get_cosmos_client()
    document = Document(document_id, content, doc_type)
    container.upsert_item(body=document.to_dict())
    return {"status": "success", "document_id": document_id}
