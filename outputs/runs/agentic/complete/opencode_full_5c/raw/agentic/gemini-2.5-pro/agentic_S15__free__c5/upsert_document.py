import json
from database_client import get_db_table
from database_models import Document


def upsert_document(document: Document):
    table = get_db_table()

    item = {
        "documentId": document.document_id,
        "version": document.version,
        "content": json.dumps(document.content),
        "userId": document.user_id,
    }

    response = table.put_item(Item=item)
    return response
