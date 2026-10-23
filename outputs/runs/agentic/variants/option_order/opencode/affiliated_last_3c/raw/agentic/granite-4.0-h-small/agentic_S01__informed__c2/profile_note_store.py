# [LATER-STEP] profile_note_store.py
# Persist onboarding notes and support metadata in Alibaba Tablestore (NoSQL) database

import os
from tablestore import SyncClient, Row, PrimaryKey, CONDITION
from tablestore.error import TableStoreError

ENDPOINT = os.getenv("ALIBABA_CLOUD_ENDPOINT")
INST_NAME = os.getenv("ALIBABA_CLOUD_INST_NAME")
ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
TABLE_NAME = os.getenv("TABLESTORE_TABLE_NAME", "OnboardingNotes")
PK_USER = "UserId"

client = SyncClient(
    ENDPOINT,
    instName=INST_NAME,
    accessKeyId=ACCESS_KEY_ID,
    accessKeySecret=ACCESS_KEY_SECRET,
)


def upsert_onboarding_note(user_id: str, payload: dict) -> None:
    """Insert or update (upsert) a JSON payload for the given user_id."""
    pk = [PrimaryKey(PK_USER, user_id)]
    row = Row(pk)
    # Convert dict to columns (simple approach: store whole JSON as a single column)
    row.add_attribute_column("Data", json.dumps(payload))
    try:
        client.put_row(table_name=TABLE_NAME, row=row, condition=CONDITION.IGNORE)
    except TableStoreError as e:
        # In production you would handle/log the error appropriately
        raise RuntimeError(f"Failed to store onboarding note: {e}")


# Example usage (uncomment to test)
# upsert_onboarding_note("user-001", {"locale": "fr", "notes": "User prefers French UI"})
# End of file
