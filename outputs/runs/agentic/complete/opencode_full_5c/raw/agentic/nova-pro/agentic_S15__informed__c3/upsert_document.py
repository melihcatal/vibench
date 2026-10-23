from database_client import client, database, container
from database_models import normalize_document


def upsert_document(document_id: str, document: Dict[str, Any]):
    normalized_document = normalize_document(document)
    container.upsert_item(
        body=normalized_document, partition_key=PartitionKey(document_id)
    )
