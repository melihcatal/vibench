# expense_record_store.py
# Persist normalized expense records in IBM Cloudant NoSQL document store
import os
import json
from ibmcloudant import CloudantClient
from document_models import ExpenseResponse

# Load credentials from environment variables
CLOUDANT_URL = os.getenv('IBM_CLOUDANT_URL')
CLOUDANT_APIKEY = os.getenv('IBM_CLOUDANT_APIKEY')

# Initialize client
client = CloudantClient(url=CLOUDANT_URL, auth=CLOUDANT_APIKEY)

def store_expense(expense: ExpenseResponse) -> dict:
    """Insert a normalized expense document into Cloudant.",
    # Use the 'invoice_id' or a generated UUID as document ID
    doc_id = expense.get('invoice_id') or str(uuid.uuid4())
    document = {
        '_id': doc_id,
        **expense  # include all normalized fields
    }
    # Insert or replace the document
    result = client.insert(doc_id, document)
    return result
