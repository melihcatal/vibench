import json
from database_client import get_database_uri, normalize_document
from database_models import DocumentRequest, DocumentResponse
from database_client import parse_response

# Managed NoSQL Document Store integration (concrete provider)
# Example implementation for Amazon DynamoDB using boto3 SDK
import boto3
from botocore.exceptions import ClientError

# Create a client once (could be configured per provider elsewhere)
client = boto3.client('dynamodb')

def upsert_document(primary_id: str, document: dict) -> DocumentResponse:
    """Upsert (create or replace) a document in the managed NoSQL store.
    Uses the environment‑identified provider URI; here we target DynamoDB.
    Args:
        primary_id: Unique identifier for the document.
        document: The full JSON payload to store.
    Returns:
        DocumentResponse containing the stored document.
    """
    # Normalize and prepare request payload per provider expectations
    normalized_doc = normalize_document(document)
    request_payload = DocumentRequest(primary_id=primary_id, fields=normalized_doc).to_dict()

    try:
        # DynamoDB `PutItem` creates a new item or replaces an existing one
        response = client.put_item(
            TableName=get_env_or_raise("DYNAMODB_TABLE_NAME"),
            Item=json.loads(json.dumps(request_payload))  # ensure correct serialization
        )
    except ClientError as e:
        raise RuntimeError(f"DynamoDB upsert failed: {e.response['Error']['Message']}")

    # Parse provider response into our common model
    raw = response.get('ResponseMetadata',{})  # placeholder; replace with actual doc fetch if needed
    return parse_response(raw)

# Helper to raise if required env var missing (shared across files)
get_env_or_raise = lambda var: 
    os.getenv(var) or (lambda: (_ for _ in ()).throw(RuntimeError(f"Missing env {var}")))()()
