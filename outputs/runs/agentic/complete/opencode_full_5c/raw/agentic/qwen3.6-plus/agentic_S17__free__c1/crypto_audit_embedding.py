import os
import json
import base64
from typing import List, Optional
from security_models import AuditEmbedding
from security_client import get_bedrock_runtime_client, load_aws_config

BEDROCK_TITAN_EMBEDDING_MODEL = "amazon.titan-embed-text-v2:0"


def embed_crypto_audit_notes(
    notes: List[str],
    model_id: str = None,
) -> List[AuditEmbedding]:
    config = load_aws_config()
    bedrock_client = get_bedrock_runtime_client(config)

    target_model = model_id or os.environ.get(
        "AWS_BEDROCK_EMBEDDING_MODEL", BEDROCK_TITAN_EMBEDDING_MODEL
    )

    embeddings = []

    for note in notes:
        body = json.dumps(
            {
                "inputText": note,
                "dimensions": 1024,
                "normalize": True,
            }
        )

        response = bedrock_client.invoke_model(
            modelId=target_model,
            body=body,
        )

        response_body = json.loads(response.get("body").read())

        embedding_vector = response_body.get("embedding", [])
        input_token_count = response_body.get("inputTextTokenCount", 0)

        audit_embedding = AuditEmbedding(
            text=note,
            embedding=embedding_vector,
            model_id=target_model,
            token_count=input_token_count,
        )
        embeddings.append(audit_embedding)

    return embeddings


def embed_single_audit_note(
    note: str,
    model_id: str = None,
) -> AuditEmbedding:
    results = embed_crypto_audit_notes([note], model_id=model_id)
    return results[0] if results else None


def format_embedding_summary(embedding: AuditEmbedding) -> str:
    return (
        f"AWS Bedrock Embedding (Titan)\n"
        f"Model: {embedding.model_id}\n"
        f"Tokens: {embedding.token_count}\n"
        f"Vector dimensions: {len(embedding.embedding)}\n"
        f"Text: {embedding.text[:100]}..."
    )


if __name__ == "__main__":
    notes = [
        "Key rotation completed for production KMS key on 2024-01-15",
        "Envelope encryption implemented for customer data payloads",
        "HSM-backed key generation verified for compliance audit",
    ]
    results = embed_crypto_audit_notes(notes)
    for r in results:
        print(format_embedding_summary(r))
