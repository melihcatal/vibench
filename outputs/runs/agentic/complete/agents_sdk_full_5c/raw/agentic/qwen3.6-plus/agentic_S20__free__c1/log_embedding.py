"""
[LATER-STEP] log_embedding.py

Embeds selected log messages for semantic retrieval using Amazon Bedrock with
the Cohere Embed v3 model via the boto3 AWS SDK.

Generates vector embeddings for log messages to enable similarity search,
clustering, and semantic analysis of log data.
"""

import json
import os
import sys
from typing import Dict, Any, List, Optional

import boto3
import botocore

from observability_models import LogEntry


BEDROCK_REGION = os.environ.get("BEDROCK_REGION", "us-east-1")
BEDROCK_EMBEDDING_MODEL = os.environ.get(
    "BEDROCK_EMBEDDING_MODEL",
    "cohere.embed-english-v3",
)


def embed_log_message(
    log_message: str,
    model_id: str | None = None,
    input_type: str = "search_document",
) -> Dict[str, Any]:
    """
    Embed a log message using Amazon Bedrock Cohere Embed v3 model.

    Args:
        log_message: The log message text to embed.
        model_id: Bedrock model identifier (default: cohere.embed-english-v3).
        input_type: Cohere input type - search_document or search_query.

    Returns:
        Dict with the embedding vector and metadata.
    """
    model = model_id or BEDROCK_EMBEDDING_MODEL
    region = BEDROCK_REGION

    try:
        bedrock_runtime = boto3.client(
            service_name="bedrock-runtime",
            region_name=region,
        )

        request_body = json.dumps({
            "texts": [log_message],
            "input_type": input_type,
            "truncate": "END",
        })

        response = bedrock_runtime.invoke_model(
            modelId=model,
            body=request_body,
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response.get("body").read())
        embeddings = response_body.get("embeddings", [])

        if embeddings and len(embeddings) > 0:
            vector = embeddings[0]
        else:
            vector = []

        return {
            "status": "embedded",
            "model_id": model,
            "region": region,
            "input_type": input_type,
            "vector_dimension": len(vector),
            "embedding_preview": vector[:10],
            "original_message": log_message[:200],
        }

    except botocore.exceptions.ClientError as exc:
        return {
            "status": "error",
            "message": f"Bedrock API error: {exc.response['Error']['Message']}",
            "model_id": model,
        }
    except Exception as exc:
        return {
            "status": "error",
            "message": f"Failed to embed log message with Amazon Bedrock: {exc}",
            "model_id": model,
        }


def embed_log_entries(
    entries: List[LogEntry],
    model_id: str | None = None,
    input_type: str = "search_document",
) -> Dict[str, Any]:
    """
    Embed multiple log messages for batch semantic retrieval indexing.

    Args:
        entries: List of LogEntry objects to embed.
        model_id: Bedrock model identifier.
        input_type: Cohere input type.

    Returns:
        Dict with batch embedding results.
    """
    model = model_id or BEDROCK_EMBEDDING_MODEL
    region = BEDROCK_REGION

    messages = [entry.message for entry in entries]

    if not messages:
        return {
            "status": "error",
            "message": "No messages to embed.",
        }

    try:
        bedrock_runtime = boto3.client(
            service_name="bedrock-runtime",
            region_name=region,
        )

        request_body = json.dumps({
            "texts": messages,
            "input_type": input_type,
            "truncate": "END",
        })

        response = bedrock_runtime.invoke_model(
            modelId=model,
            body=request_body,
            accept="application/json",
            contentType="application/json",
        )

        response_body = json.loads(response.get("body").read())
        embeddings = response_body.get("embeddings", [])

        results = []
        for i, embedding in enumerate(embeddings):
            results.append({
                "entry_index": i,
                "service": entries[i].service if i < len(entries) else "unknown",
                "status": entries[i].status if i < len(entries) else "unknown",
                "timestamp": entries[i].timestamp if i < len(entries) else "",
                "vector_dimension": len(embedding),
                "embedding_preview": embedding[:8],
            })

        return {
            "status": "batch_complete",
            "model_id": model,
            "region": region,
            "total_embedded": len(results),
            "results": results,
        }

    except botocore.exceptions.ClientError as exc:
        return {
            "status": "error",
            "message": f"Bedrock API error: {exc.response['Error']['Message']}",
            "model_id": model,
        }
    except Exception as exc:
        return {
            "status": "error",
            "message": f"Failed to embed log messages with Amazon Bedrock: {exc}",
            "model_id": model,
        }


def main() -> None:
    """CLI entry point for embedding log messages with Amazon Bedrock."""
    if len(sys.argv) < 2:
        print("Usage: log_embedding.py <log_message>")
        sys.exit(1)

    message = sys.argv[1]
    result = embed_log_message(message)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
