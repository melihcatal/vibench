import os
import json
from typing import List
from security_client import get_bedrock_runtime_client
from security_models import AuditNoteEmbedding

def embed_audit_note(note_id: str, note_text: str, region: str = 'us-east-1', model_id: str = 'amazon.titan-embed-text-v1') -> AuditNoteEmbedding:
    """
    Embeds crypto audit notes for semantic search using Amazon Titan Embeddings via Bedrock Runtime.
    """
    bedrock_runtime_client = get_bedrock_runtime_client(region)
    
    body = json.dumps({"inputText": note_text})
    
    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )
    
    response_body = json.loads(response.get('body').read())
    embedding = response_body.get('embedding')
    
    return AuditNoteEmbedding(note_id=note_id, note_text=note_text, embedding=embedding)

if __name__ == '__main__':
    # This is example usage and should not be part of the final submission.
    # Ensure AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and AWS_REGION are set in environment variables.
    
    # example_note_id = "AUDIT-001"
    # example_note_text = "Performed routine key rotation for production KMS key 'alias/prod/web-app-key' on 2023-10-27."
    
    # audit_embedding = embed_audit_note(example_note_id, example_note_text)
    # print(f"Audit Note ID: {audit_embedding.note_id}")
    # print(f"Audit Note Text: '{audit_embedding.note_text}'")
    # print(f"Embedding (first 5 values): {audit_embedding.embedding[:5]}...")
    # print(f"Embedding dimension: {len(audit_embedding.embedding)}")
