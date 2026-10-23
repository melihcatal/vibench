DO NOT REMOVE THIS LINE - CONTENT BELOW IS EDITABLE BY THE ASSISTANT

Purpose: Persist onboarding notes and metadata in a managed document store using Alibaba Tablestore (OTS)

---

```python
import os
from tablestore import SyncClient, Row, PrimaryKey, SCHEMALESS
from typing import Dict, Any

# Load Tablestore credentials from environment
OTS_ENDPOINT = os.getenv('OTS_ENDPOINT')
OTS_INSTANCE = os.getenv('OTS_INSTANCE')
OTS_ACCESS_KEY_ID = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID')
OTS_ACCESS_KEY_SECRET = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET')
TABLE_NAME = 'onboarding_notes'

# Initialize Tablestore client
ots_client = SyncClient(
    endpoint=OTS_ENDPOINT,
    instance=OTS_INSTANCE,
    access_key_id=OTS_ACCESS_KEY_ID,
    access_key_secret=OTS_ACCESS_KEY_SECRET
)

def store_onboarding(note_id: str, data: Dict[str, Any]) -> None:
    """Persist onboarding notes and associated metadata.
    Overwrites any existing row with the same primary key.
    """
    table = ots_client.get_table(meta=TABLE_NAME)
    # Use a simple schemaless design: all fields in one attribute named 'document'
    row = Row(
        primary_key=[('note_id', note_id)],
        attribute_columns=[('document', data)]
    )
    # Upsert (insert or replace)
    ots_client.put_row(table, row)


def get_onboarding(note_id: str) -> Dict[str, Any] | None:
    """Retrieve onboarding payload by note_id.
    Returns decoded document dict or None if missing.
    """
    table = ots_client.get_table(meta=TABLE_NAME)
    pk = PrimaryKey([('note_id', note_id)])
    response = ots_client.get_row(table, pk)
    if response.row is None:
        return None
    # The 'document' attribute holds the JSON payload
    return response.row.attribute_columns[0][1] if response.row.attribute_columns else {}
```