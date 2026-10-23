"""
Embed crypto audit notes for semantic search using AWS Bedrock.

Uses the Amazon Bedrock Runtime API (bedrock-runtime.{region}.amazonaws.com)
with the boto3 SDK to generate vector embeddings of cryptographic audit
notes, enabling semantic search over security documentation and logs.

Model: amazon.titan-embed-text-v1 (Titan Embeddings G1 - Text)
"""

import os
import logging
from typing import Optional, Dict, Any, List
import json

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from security_models import (
    AuditNoteRequest,
    EmbeddingResponse,
)

logger = logging.getLogger(__name__)

BEDROCK_MODEL_ID = "amazon.titan-embed-text-v1"
BEDROCK_ENDPOINT_TEMPLATE = "bedrock-runtime.{region}.amazonaws.com"


def get_bedrock_runtime_client(region: Optional[str] = None):
    """
    Initialize an Amazon Bedrock Runtime boto3 client.

    Provider: Amazon Bedrock (bedrock-runtime.{region}.amazonaws.com)
    Model: amazon.titan-embed-text-v1
    """
    resolved_region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    credentials = {}
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    if access_key:
        credentials["aws_access_key_id"] = access_key
    if secret_key:
        credentials["aws_secret_access_key"] = secret_key

    config = Config(
        retries={"max_attempts": 3, "mode": "standard"},
        connect_timeout=10,
        read_timeout=60,
    )

    return boto3.client(
        "bedrock-runtime",
        region_name=resolved_region,
        config=config,
        **credentials,
    )


def embed_audit_note(
    note_text: str,
    key_id: Optional[str] = None,
    event_type: str = "audit",
    model_id: Optional[str] = None,
    client=None,
    region: Optional[str] = None,
) -> EmbeddingResponse:
    """
    Embed a crypto audit note text into a vector for semantic search.

    Provider: Amazon Bedrock (bedrock-runtime.{region}.amazonaws.com)
    Model: amazon.titan-embed-text-v1

    Args:
        note_text: The audit note text to embed.
        key_id: Optional KMS key ID associated with the note.
        event_type: Event type tag (default: 'audit').
        model_id: Optional model override (default: amazon.titan-embed-text-v1).
        client: Optional pre-initialized Bedrock Runtime client.
        region: Optional AWS region override.

    Returns:
        EmbeddingResponse with the embedding vector.

    Raises:
        ValueError: If note_text is empty.
        ClientError: On Bedrock API failure.
    """
    if not note_text or len(note_text.strip()) == 0:
        raise ValueError("note_text cannot be empty")

    resolved_region = region or os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
    endpoint = BEDROCK_ENDPOINT_TEMPLATE.format(region=resolved_region)

    if client is None:
        client = get_bedrock_runtime_client(resolved_region)

    use_model_id = model_id or BEDROCK_MODEL_ID

    logger.info(
        "Calling Amazon Bedrock InvokeModel for embeddings (model: %s, endpoint: %s)",
        use_model_id,
        endpoint,
    )

    body = json.dumps({
        "inputText": note_text,
    })

    response = client.invoke_model(
        modelId=use_model_id,
        body=body,
        accept="application/json",
        contentType="application/json",
    )

    response_body = json.loads(response.get("body").read())
    embedding = response_body.get("embedding", [])
    input_token_count = response_body.get("inputTextTokenCount", 0)

    result = EmbeddingResponse(
        vector=embedding,
        model=use_model_id,
        text=note_text,
        usage={
            "input_tokens": input_token_count,
            "output_tokens": 0,
            "total_tokens": input_token_count,
        },
    )

    logger.info(
        "Embedding generated via Amazon Bedrock model %s: %d dimensions, %d input tokens",
        use_model_id,
        len(embedding),
        input_token_count,
    )

    return result


def embed_from_request(request: AuditNoteRequest, client=None) -> EmbeddingResponse:
    """
    Embed using an AuditNoteRequest dataclass.

    Args:
        request: AuditNoteRequest with note text and metadata.
        client: Optional pre-initialized Bedrock Runtime client.

    Returns:
        EmbeddingResponse with the embedding vector.
    """
    return embed_audit_note(
        note_text=request.note_text,
        key_id=request.key_id,
        event_type=request.event_type,
        client=client,
    )


def batch_embed_notes(
    notes: List[str],
    model_id: Optional[str] = None,
    region: Optional[str] = None,
) -> List[EmbeddingResponse]:
    """
    Embed multiple audit notes sequentially.

    Provider: Amazon Bedrock (bedrock-runtime.{region}.amazonaws.com)
    Model: amazon.titan-embed-text-v1

    Args:
        notes: List of audit note strings to embed.
        model_id: Optional model override.
        region: Optional AWS region override.

    Returns:
        List of EmbeddingResponse objects.
    """
    results = []
    client = get_bedrock_runtime_client(region)

    for i, note in enumerate(notes):
        try:
            result = embed_audit_note(
                note_text=note,
                model_id=model_id,
                client=client,
                region=region,
            )
            results.append(result)
        except ClientError as e:
            logger.warning("Failed to embed note %d: %s", i + 1, str(e))
            continue

    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    sample_note = os.environ.get(
        "AUDIT_EMBEDDING_TEST_NOTE",
        "AES-256 key rotation completed for production environment on 2024-01-15"
    )
    if sample_note:
        result = embed_audit_note(sample_note)
        print(f"Model: {result.model}")
        print(f"Vector dimensions: {len(result.vector)}")
        print(f"Input tokens: {result.usage['input_tokens']}")
        print(f"Vector (first 5): {result.vector[:5]}")
    else:
        print("No test note available.")
