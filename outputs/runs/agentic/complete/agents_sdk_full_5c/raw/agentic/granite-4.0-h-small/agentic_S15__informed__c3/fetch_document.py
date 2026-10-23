import os
import json
from database_client import fetch_document
from database_models import EXAMPLE_ITEM

# ------------------------------------------------------------
# fetch_document.py
# ------------------------------------------------------------
db_name = os.getenv('CLOUDANT_DB', 'mydb')

# Example: fetch a user profile by its primary identifier
def main():
    # Assuming the user profile has _id = 'user-123'
    user_id = 'user-123'
    doc = fetch_document(db_name, user_id)
    if doc:
        print(f"Fetched document: {doc}")
    else:
        print("Document not found.")

if __name__ == "__main__":
    main()
