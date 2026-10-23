from database_client import get_table, make_key
from database_models import DocumentFetchRequest


def fetch_document(request: DocumentFetchRequest):
    table = get_table()
    response = table.get_item(Key=make_key(request.document_id))
    return response.get("Item")
