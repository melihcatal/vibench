from typing import List
from database_client import get_db_collection
from database_models import Document

def query_documents_by_author(author: str) -> List[Document]:
    """
    Queries for documents in MongoDB Atlas written by a specific author.

    Args:
        author: The author to query for.

    Returns:
        A list of Document objects matching the query.
    """
    collection = get_db_collection()
    documents = []
    
    # The find method returns a cursor that we can iterate over
    cursor = collection.find({"author": author})
    
    for doc_data in cursor:
        documents.append(Document.from_dict(doc_data))
        
    print(f"Found {len(documents)} documents for author '{author}'.")
    return documents
