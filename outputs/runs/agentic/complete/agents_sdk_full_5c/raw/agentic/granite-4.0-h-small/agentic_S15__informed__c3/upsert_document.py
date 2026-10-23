import os
import json
from database_client import upsert_document, fetch_document, query_documents, conditional_update
from database_models import EXAMPLE_USER_PROFILE, EXAMPLE_ITEM

# ------------------------------------------------------------
# upsert_document.py
# ------------------------------------------------------------
db_name = os.getenv('CLOUDANT_DB', 'mydb')

# Example: upsert a user profile document using the Document helper
def main():
    doc = EXAMPLE_USER_PROFILE
    upsert_document(db_name, doc["_id"], doc)
    print(f"Document {_id=} upserted.")

if __name__ == "__main__":
    main()
