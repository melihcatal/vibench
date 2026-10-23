from security_client import SecurityClient
from security_models import CryptoAuditEmbeddingRequest, CryptoAuditEmbeddingResponse
import json


def embed_crypto_audit_notes(
    request: CryptoAuditEmbeddingRequest,
) -> CryptoAuditEmbeddingResponse:
    client = SecurityClient()
    embeddings = []
    for note in request.audit_notes:
        body = json.dumps({"inputText": note})
        response = client.bedrock_runtime_client.invoke_model(
            body=body,
            modelId="amazon.titan-embed-text-v1",
            accept="application/json",
            contentType="application/json",
        )
        response_body = json.loads(response.get("body").read())
        embeddings.append(response_body.get("embedding"))

    return CryptoAuditEmbeddingResponse(embeddings=embeddings)
