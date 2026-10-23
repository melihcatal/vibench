import os
import json
from database_client import query_documents

# ------------------------------------------------------------
# query_documents.py
# ------------------------------------------------------------
db_name = os.getenv('CLOUDANT_DB', 'mydb')

# Example: query all items in the 'test' category
def main():
    selector = {
        'selector': {
            'category': 'test'
        }
    }
    results = query_documents(db_name, selector)
    print(f"Found {len(results)} documents matching selector:", json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
