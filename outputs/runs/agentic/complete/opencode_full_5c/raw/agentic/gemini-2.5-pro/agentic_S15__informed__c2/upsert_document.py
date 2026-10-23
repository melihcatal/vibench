from database_client import get_table
from database_models import Document, UpsertResponse


def upsert_document(document: Document) -> UpsertResponse:
    """
    Upserts a document into DynamoDB.

    Args:
        document: The document to upsert.

    Returns:
        An UpsertResponse indicating the result.
    """
    if "version" not in document:
        document["version"] = 1

    table = get_table()
    try:
        table.put_item(Item=document)
        return {
            "success": True,
            "document_id": document["document_id"],
            "version": document["version"],
        }
    except Exception as e:
        print(f"Error upserting document: {e}")
        return {
            "success": False,
            "document_id": document["document_id"],
            "version": document.get("version", 0),
        }
