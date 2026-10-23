from database_client import get_firestore_client
from database_models import Document, DocumentQuery

def query_documents(collection_name: str, query: DocumentQuery) -> list[Document]:
    """Queries documents by a field value or partition-style key from Firestore.

    Args:
        collection_name: The name of the Firestore collection.
        query: The DocumentQuery object specifying the field and value to query.

    Returns:
        A list of Document objects that match the query.
    """
    db = get_firestore_client()
    docs_ref = db.collection(collection_name)
    
    query_results = docs_ref.where(query.field, "==", query.value).stream()
    
    documents = []
    for doc in query_results:
        print(f"{doc.id} => {doc.to_dict()}")
        documents.append(Document.from_firestore_document(doc))
    
    return documents
