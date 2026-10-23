import os
import boto3
import json
from typing import List, Dict, Any
from botocore.exceptions import ClientError
from security_models import AuditNote

class AWSBedrockClient:
    def __init__(self):
        self.client = boto3.client('bedrock-runtime')
        self.model_id = 'amazon.titan-embed-text-v1'  # Example embedding model ID

    def get_text_embedding(self, text: str) -> List[float]:
        try:
            body = json.dumps({"inputText": text})
            response = self.client.invoke_model(
                body=body,
                modelId=self.model_id,
                accept='application/json',
                contentType='application/json'
            )
            response_body = json.loads(response.get('body').read())
            return response_body.get('embedding')
        except ClientError as e:
            print(f"Error getting text embedding: {e}")
            raise

def embed_secret_audit_notes(audit_notes: List[AuditNote]) -> Dict[str, List[float]]:
    bedrock_client = AWSBedrockClient()
    embeddings = {}
    for note in audit_notes:
        if note.content:
            embeddings[note.note_id] = bedrock_client.get_text_embedding(note.content)
    return embeddings
