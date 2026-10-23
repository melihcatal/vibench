import json

from security_client import get_bedrock_runtime_client
from security_models import CryptoAuditEmbeddingRequest, CryptoAuditEmbeddingResponse


def embed_audit_notes(
    request: CryptoAuditEmbeddingRequest,
) -> CryptoAuditEmbeddingResponse:
    bedrock_runtime_client = get_bedrock_runtime_client()
    try:
        # The model ID for Amazon Titan Embeddings can vary. Common ones are 'amazon.titan-embed-text-v1'
        # Refer to AWS Bedrock documentation for the latest model IDs.
        model_id = "amazon.titan-embed-text-v1"  # Concrete model identifier

        body = json.dumps({"inputText": request.notes})

        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response.get("body").read())
        embedding = response_body.get("embedding")

        if not embedding:
            raise ValueError("Embedding not found in the response from Bedrock.")

        return CryptoAuditEmbeddingResponse(embedding=embedding)
    except Exception as e:
        raise RuntimeError(
            f"Error generating embedding with Amazon Titan Embeddings via Bedrock: {e}"
        )
