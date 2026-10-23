import os
from typing import List, Dict, Any
import boto3
from botocore.config import Config
import json


def embed_document_sections(sections: List[str]) -> List[Dict[str, Any]]:
    """
    Embed extracted document sections for semantic retrieval using Amazon Titan Embeddings.

    Args:
        sections: List of document text sections to embed

    Returns:
        List of embeddings with metadata
    """
    # Initialize Bedrock Runtime client for Titan embeddings
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region_name = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError(
            "AWS credentials not found. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
        )

    bedrock_client = boto3.client(
        "bedrock-runtime",
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        config=Config(retries={"max_attempts": 3}),
    )

    embeddings = []

    for i, text in enumerate(sections):
        if not text or len(text.strip()) == 0:
            continue

        # Prepare request for Titan Embeddings model
        # Using amazon.titan-embed-text-v2:0 model
        request_body = json.dumps(
            {
                "inputText": text,
                "dimensions": 1024,  # Titan v2 supports configurable dimensions
                "normalize": True,
            }
        )

        try:
            response = bedrock_client.invoke_model(
                modelId="amazon.titan-embed-text-v2:0",
                contentType="application/json",
                accept="application/json",
                body=request_body,
            )

            response_body = json.loads(response["body"].read())

            embedding = response_body.get("embedding", [])

            embeddings.append(
                {
                    "section_index": i,
                    "text_preview": text[:100] + "..." if len(text) > 100 else text,
                    "embedding": embedding,
                    "embedding_dimensions": len(embedding),
                    "model": "amazon.titan-embed-text-v2:0",
                    "provider": "Amazon Bedrock",
                }
            )

        except Exception as e:
            embeddings.append(
                {
                    "section_index": i,
                    "text_preview": text[:100] + "..." if len(text) > 100 else text,
                    "error": str(e),
                    "model": "amazon.titan-embed-text-v2:0",
                    "provider": "Amazon Bedrock",
                }
            )

    return embeddings


def embed_with_metadata(sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Embed document sections with additional metadata.

    Args:
        sections: List of document sections with text and metadata

    Returns:
        List of embeddings with full metadata
    """
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region_name = os.getenv("AWS_REGION", "us-east-1")

    bedrock_client = boto3.client(
        "bedrock-runtime",
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    results = []

    for section in sections:
        text = section.get("text", "")
        if not text:
            continue

        # Truncate text if too long (Titan has token limits)
        if len(text) > 8000:
            text = text[:8000]

        request_body = json.dumps(
            {"inputText": text, "dimensions": 1024, "normalize": True}
        )

        try:
            response = bedrock_client.invoke_model(
                modelId="amazon.titan-embed-text-v2:0", body=request_body
            )

            response_body = json.loads(response["body"].read())
            embedding = response_body.get("embedding", [])

            result = section.copy()
            result.update(
                {
                    "embedding": embedding,
                    "embedding_dimensions": len(embedding),
                    "embedding_model": "amazon.titan-embed-text-v2:0",
                    "embedding_provider": "Amazon Bedrock",
                    "has_embedding": True,
                }
            )

            results.append(result)

        except Exception as e:
            result = section.copy()
            result.update(
                {
                    "embedding_error": str(e),
                    "embedding_model": "amazon.titan-embed-text-v2:0",
                    "embedding_provider": "Amazon Bedrock",
                    "has_embedding": False,
                }
            )
            results.append(result)

    return results


def batch_embed_documents(documents: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Batch embed multiple documents for efficient processing.

    Args:
        documents: List of documents with text content

    Returns:
        Batch embedding results
    """
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region_name = os.getenv("AWS_REGION", "us-east-1")

    bedrock_client = boto3.client(
        "bedrock-runtime",
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    successful = 0
    failed = 0
    all_embeddings = []

    for doc in documents:
        text = doc.get("text", "")
        doc_id = doc.get("id", "unknown")

        if not text:
            failed += 1
            continue

        request_body = json.dumps(
            {
                "inputText": text[:8000],  # Truncate if too long
                "dimensions": 1024,
                "normalize": True,
            }
        )

        try:
            response = bedrock_client.invoke_model(
                modelId="amazon.titan-embed-text-v2:0", body=request_body
            )

            response_body = json.loads(response["body"].read())
            embedding = response_body.get("embedding", [])

            all_embeddings.append(
                {
                    "document_id": doc_id,
                    "embedding": embedding,
                    "text_preview": text[:100] + "..." if len(text) > 100 else text,
                }
            )

            successful += 1

        except Exception as e:
            failed += 1

    return {
        "embeddings": all_embeddings,
        "summary": {
            "total_documents": len(documents),
            "successful_embeddings": successful,
            "failed_embeddings": failed,
            "success_rate": (successful / len(documents) * 100) if documents else 0,
        },
        "model": "amazon.titan-embed-text-v2:0",
        "provider": "Amazon Bedrock",
        "embedding_dimensions": 1024,
    }
