import os
import json
from database_client import conditional_update

# ------------------------------------------------------------
# conditional_update.py
# ------------------------------------------------------------
db_name = os.getenv('CLOUDANT_DB', 'mydb')

# Example: safely update a user profile only if the revision matches
# Simulate expected revision from a previous fetch
def main():
    user_id = 'user-123'
    # Fetch the current revision first
    doc = fetch_document(db_name, user_id)
    expected_rev = doc.get('_rev') if doc else None
    if not expected_rev:
        print('Document not found; cannot perform conditional update.')
        return
    # Update payload
    update_payload = {
        'email': 'john.doe@example.com'
    }
    conditional_update(db_name, user_id, {'rev': expected_rev}, update_payload)
    print(f"Document {user_id} conditionally updated.")

if __name__ == "__main__":
    main()
