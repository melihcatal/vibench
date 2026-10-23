import json
import os
from google.cloud import secretmanager
from google.cloud.aiplatform import embedding as aip_embedding

from security_client import get_config
from security_models import SecretDef

def secret_audit_embedding(secret_def: SecretDef, audit_note: str) -> str:
    """Embedding of secret audit notes using AWS Bedrock Titan embeddings via boto3.
    Returns a UUID that can be used for semantic search.
    """
    # Store audit note as a Secret Manager secret for Titan embedding reference
    client = secretmanager.SecretManagerServiceClient()
    audit_secret_name = f"projects/{os.getenv('GCP_PROJECT')}/secrets/{secret_def['name']}-audit/versions/latest"
    try:
        client.get_secret(name=audit_secret_name)
    except Exception:
        parent = f"projects/{os.getenv('GCP_PROJECT')}/secrets"
        client.create_secret(parent=parent, secret_id=secret_def['name']+'-audit', secret={})
    client.add_secret_version(name=audit_secret_name, payload={'data': audit_note.encode('utf-8')})

    # Embedding call using Bedrock Titan
    from botocore.client import Config as BotoConfig
    bedrock = boto3.client('bedrock-runtime', region_name='us-east-1', config=BotoConfig(timeout=120))
    prompt = {
        "inputs": [
            {
                "text": audit_note
            }
        ],
        "parameters": {
            "maxOutputTokens": 256,
            "temperature": 0.0
        }
    }
    response = bedrock.invoke_model(model_id='amazon.titan-text-express-v1', body=json.dumps(prompt))
    embedding_id = response['modelId']  # placeholder; real embedding could be extracted from response
    return embedding_id
