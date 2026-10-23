# [SAME-SCENARIO] upsert_document.py
import json
from database_client import NoSQLClient

def upsert_document(doc_id, document):
    """Upsert a JSON document in the managed NoSQL store.

    Args:
        doc_id (str): Primary identifier for the document.
        document (dict): JSON‑serializable document payload.
    """
    client = NoSQLClient()
    payload = json.dumps(document)
    client.put_item(TableName=client.table_name,
                    Key={'id': {'S': doc_id}},
                    Item={'content': {'S': payload}})
    print(f"Document {doc_id} upserted.")