from database_client import get_collection
from database_models import Document, Optional

def fetch_document(doc_id: str) -> Optional[Document]:
    coll = get_collection()
    return coll.find_one({"_id": doc_id})