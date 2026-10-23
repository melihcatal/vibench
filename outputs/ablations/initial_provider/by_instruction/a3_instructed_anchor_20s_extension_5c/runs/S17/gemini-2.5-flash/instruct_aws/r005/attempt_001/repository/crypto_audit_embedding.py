import os
import boto3
import json

class CryptoAuditEmbeddingRequest:
    def __init__(self, audit_note: str):
        self.audit_note = audit_note

class CryptoAuditEmbeddingResponse:
    def __init__(self, embedding: list):
        self.embedding = embedding

# Placeholder for a SageMaker endpoint name for embeddings
SAGEMAKER_ENDPOINT_NAME = os.environ.get("SAGEMAKER_EMBEDDING_ENDPOINT", "your-sagemaker-embedding-endpoint")

def embed_crypto_audit_note(request: CryptoAuditEmbeddingRequest) -> CryptoAuditEmbeddingResponse:
    region_name = os.environ.get("AWS_REGION", "us-east-1")
    sagemaker_runtime_client = boto3.client("sagemaker-runtime", region_name=region_name)

    embedding = []
    try:
        # The payload structure depends on the specific SageMaker model deployed.
        # This is a common structure for text embedding models.
        payload = {"inputs": request.audit_note}
        response = sagemaker_runtime_client.invoke_endpoint(
            EndpointName=SAGEMAKER_ENDPOINT_NAME,
            ContentType='application/json',
            Body=json.dumps(payload)
        )

        result = json.loads(response['Body'].read().decode())
        # The exact key for the embedding depends on the model output.
        # Assuming the embedding is directly in 'embedding' key or similar.
        embedding = result.get('embedding', []) or result.get('sentence_embedding', [])

    except Exception as e:
        # In a real scenario, you'd want more robust error handling and logging.
        print(f"Error invoking SageMaker endpoint: {e}")
        # Return an empty embedding or raise the exception as appropriate.

    return CryptoAuditEmbeddingResponse(
        embedding=embedding
    )