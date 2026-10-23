from typing import Optional
from database_client import get_db_collection
from database_models import Document

def fetch_document(doc_id: str) -> Optional[Document]:
    """
    Fetches a single document from MongoDB Atlas by its _id.

    Args:
        doc_id: The unique identifier of the document.

    Returns:
        A Document object if found, otherwise None.
    """
    collection = get_db_collection()
    
    # find_one is the standard pymongo method to retrieve a single document
    document_data = collection.find_one({"_id": doc_id})
    
    if document_data:
        return Document.from_dict(document_data)
    else:
        print(f"Document with ID '{doc_id}' not found.")
        return None
