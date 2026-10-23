import json

from azure.cosmos import exceptions

from database_client import get_container
from database_models import FetchDocumentResponse


def fetch_document(document_id: str):
    container = get_container()
    try:
        document = container.read_item(item=document_id, partition_key=document_id)
        return FetchDocumentResponse(found=True, document=document)
    except exceptions.CosmosResourceNotFoundError:
        return FetchDocumentResponse(found=False, document=None)


def main(document_id: str) -> str:
    response = fetch_document(document_id)
    return json.dumps({"found": response.found, "document": response.document})
