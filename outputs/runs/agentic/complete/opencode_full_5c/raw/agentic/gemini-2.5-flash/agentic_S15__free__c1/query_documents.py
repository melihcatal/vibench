from database_client import get_collection
from database_models import QueryDocumentsRequest, DocumentResponse, Document
from typing import List


def query_documents(request: QueryDocumentsRequest) -> List[DocumentResponse]:
    collection = get_collection()
    field_name = request.field_name
    field_value = request.field_value

    query = {f"content.{field_name}": field_value}  # Query within the 'content' field

    results = collection.find(query)
    documents = [
        DocumentResponse(
            document=Document(**doc), message="Document fetched successfully."
        )
        for doc in results
    ]

    if not documents:
        return [
            DocumentResponse(
                document=None, message="No documents found matching the query."
            )
        ]

    return documents
