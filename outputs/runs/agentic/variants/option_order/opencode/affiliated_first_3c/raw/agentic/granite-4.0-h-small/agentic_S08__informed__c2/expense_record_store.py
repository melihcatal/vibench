# expense_record_store.py
# [LATER-STEP]
# Persist normalized expense records in IBM Cloudant NoSQL store.

import json
from ibmcloudant import CloudantV1
from ibmcloudant.cloudant_v1 import (
    CreateDatabaseOptions,
    CreateDocumentOptions,
    Document,
)

# Cloudant credentials (environment variables)
CLOUDANT_URL = os.getenv("IBM_CLOUDANT_URL")
CLOUDANT_APIKEY = os.getenv("IBM_CLOUDANT_APIKEY")

# Initialise Cloudant client
cloudant_client = CloudantV1(
    url=CLOUDANT_URL,
    disable_ssl_verification=False,
    headers={"apiKey": CLOUDANT_APIKEY},
)

# Ensure the expense database exists
EXPENSE_DB = "expense_records"
cloudant_client.create_database(CreateDatabaseOptions(db_name=EXPENSE_DB))


def store_expense(record: Dict[str, Any]) -> None:
    """Insert a normalized expense document into Cloudant.

    The document will be saved under a generated UUID `_id`.
    """
    doc = Document.from_dict(record)
    # Use Cloudant's helper to create the document (auto‑generates _id)
    cloudant_client.create_document(
        CreateDocumentOptions(db_name=EXPENSE_DB, body=doc.to_json())
    )
    print(f"Stored expense: {record['vendor_or_merchant']} ({record['date']})")


# Example usage (remove in production)
if __name__ == "__main__":
    sample = {
        "vendor_or_merchant": "Acme Corp",
        "date": "2024-05-10",
        "total": 250.0,
        "tax": 12.0,
        "line_items": ["Widgets - 100.00", "Gadgets - 150.00"],
    }
    store_expense(sample)
