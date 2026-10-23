import os
from ibmcloudant import CloudantClient

# Load credentials from environment variables
cloudant_url = os.getenv('IBM_CLOUDANT_URL')
cloudant_apikey = os.getenv('IBM_CLOUDANT_APIKEY')

# Initialize the Cloudant client
client = CloudantClient(url=cloudant_url, api_key=cloudant_apikey)

def get_db(name):
    \"Retrieve or create a database by name.\""
    return client.database(name, throw_on_exist=False)

def upsert_document(db_name, doc_id, data):
    \"Upsert a JSON document into the specified database.\""
    db = get_db(db_name)
    # Ensure the document has an _id field
    if '_id' not in data:
        data['_id'] = doc_id
    # Upsert operation – create or replace
    db.create_document(data)

def fetch_document(db_name, doc_id):
    \"Fetch a document by its _id from the specified database.\""
    db = get_db(db_name)
    doc = db.get_document(doc_id, ignore_missing=True)
    return doc.get('_source', None)

def query_documents(db_name, selector):
    \"Query documents using a Cloudant selector (JSON query).\""
    db = get_db(db_name)
    # Use the query method with Cloudant's selector syntax
    result = db.get_query_result(selector=selector)
    return result['docs']

def conditional_update(db_name, doc_id, condition, update_payload):
    \"Apply a conditional or version-aware update.\""
    db = get_db(db_name)
    doc = db.get_document(doc_id, ignore_missing=True)
    if doc:
        # Ensure the condition matches (e.g., revision)
        if doc.get('_rev') == condition.get('rev'):
            # Merge updates
            merged = {**doc.get('_source', {}), **update_payload}
            # Add _rev for conditional write
            merged['_rev'] = doc['_rev']
            db.create_document(merged)
        else:
            raise ValueError('Conditional check failed: revision mismatch')
    else:
        raise ValueError('Document not found for conditional update')
