"""Embed platform outputs for evaluation or retrieval using Amazon Titan Embeddings."""

from typing import List, Dict, Any

from model_client import (
    load_aws_credentials,
    create_bedrock_client,
)
from model_models import EmbeddingResult


def embed_platform_output(
    text: str,
    model_id: str = "amazon.titan-embed-text-v2:0",
    region: str = "us-east-1",
) -> EmbeddingResult:
    """Generate embeddings for platform model output using Amazon Titan Embeddings.

    Uses the boto3 bedrock-runtime client to call the InvokeModel API
    for Amazon Titan Embeddings (amazon.titan-embed-text-v2:0 or
    amazon.titan-embed-text-v1) to produce vector embeddings suitable
    for semantic search, evaluation, or retrieval-augmented generation.

    Amazon Bedrock endpoint: bedrock-runtime.{region}.amazonaws.com
    """
    credentials, aws_region = load_aws_credentials()
    effective_region = region or aws_region

    client = create_bedrock_client(credentials=credentials, region=effective_region)

    invoke_kwargs: Dict[str, Any] = {
        "modelId": model_id,
        "contentType": "application/json",
        "accept": "application/json",
    }

    import json
    body = {"inputText": text}
    invoke_kwargs["body"] = json.dumps(body)

    response = client.invoke_model(**invoke_kwargs)

    response_body = json.loads(response.get("body").read())

    embedding = response_body.get("embedding", [])
    input_tokens = response_body.get("inputTextTokenCount", 0)

    dimensions = len(embedding) if embedding else 0

    return EmbeddingResult(
        text=text,
        embedding=embedding,
        model_id=model_id,
        token_count=input_tokens,
        dimensions=dimensions,
    )


def embed_multiple_outputs(
    texts: List[str],
    model_id: str = "amazon.titan-embed-text-v2:0",
    region: str = "us-east-1",
) -> List[EmbeddingResult]:
    """Embed multiple platform model outputs using Amazon Titan Embeddings.

    Calls the Amazon Bedrock Titan embedding model for each text
    individually via the bedrock-runtime InvokeModel API.
    """
    results: List[EmbeddingResult] = []
    for text in texts:
        result = embed_platform_output(text, model_id=model_id, region=region)
        results.append(result)
    return results


def embed_with_dimensions(
    text: str,
    model_id: str = "amazon.titan-embed-text-v2:0",
    dimensions: int = 256,
    region: str = "us-east-1",
) -> EmbeddingResult:
    """Generate embeddings with specified output dimensions on Amazon Titan.

    Uses Amazon Titan Embeddings v2 (amazon.titan-embed-text-v2:0)
    which supports configurable output dimensions (256, 512, 1024).
    """
    credentials, aws_region = load_aws_credentials()
    effective_region = region or aws_region

    client = create_bedrock_client(credentials=credentials, region=effective_region)

    import json
    body = {
        "inputText": text,
        "dimensions": dimensions,
        "normalize": True,
    }

    response = client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body),
    )

    response_body = json.loads(response.get("body").read())

    embedding = response_body.get("embedding", [])
    input_tokens = response_body.get("inputTextTokenCount", 0)

    return EmbeddingResult(
        text=text,
        embedding=embedding,
        model_id=model_id,
        token_count=input_tokens,
        dimensions=dimensions,
    )
