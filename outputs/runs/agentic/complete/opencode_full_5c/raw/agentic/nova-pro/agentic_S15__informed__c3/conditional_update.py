from database_client import client, database, container
from database_models import normalize_document


def conditional_update(document_id: str, document: Dict[str, Any]):
    normalized_document = normalize_document(document)
    container.replace_item(
        item=document_id,
        body=normalized_document,
        partition_key=PartitionKey(document_id),
    )
