from database_client import client, database, container
from database_models import parse_response


def fetch_document(document_id: str):
    try:
        item = container.read_item(item=document_id, partition_key=document_id)
        return parse_response(item)
    except Exception as e:
        print(f"Error fetching document: {e}")
        return None
