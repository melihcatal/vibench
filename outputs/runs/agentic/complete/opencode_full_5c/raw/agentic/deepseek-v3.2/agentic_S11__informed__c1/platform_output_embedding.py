import os
from typing import List, Dict, Any
import boto3
import json
from botocore.exceptions import ClientError


def embed_platform_output(
    text: str, model_id: str = "amazon.titan-embed-text-v2:0"
) -> Dict[str, Any]:
    """Embed platform outputs using Amazon Titan Embeddings via Bedrock Runtime."""

    # Initialize AWS Bedrock Runtime client
    bedrock_client = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    try:
        # Prepare request for Titan Embeddings model
        request_body = json.dumps(
            {
                "inputText": text,
                "dimensions": 1024,  # Titan Embeddings v2 supports dimension configuration
                "normalize": True,
            }
        )

        # Invoke the Titan Embeddings model
        response = bedrock_client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=request_body,
        )

        # Parse response
        response_body = json.loads(response["body"].read())

        # Extract embedding vector
        embedding = response_body.get("embedding", [])

        # Extract metadata
        dimensions = len(embedding)
        input_token_count = response_body.get("inputTextTokenCount", 0)

        return {
            "provider": "amazon-bedrock",
            "service": "TitanEmbeddings",
            "model_id": model_id,
            "embedding": embedding,
            "dimensions": dimensions,
            "input_token_count": input_token_count,
            "text_length": len(text),
            "normalized": True,
        }

    except ClientError as e:
        print(f"Amazon Bedrock error: {e}")

        # Fallback to simple embedding (not for production)
        return {
            "provider": "fallback-simple",
            "service": "simple-embedding",
            "model_id": "fallback",
            "embedding": [0.1] * 128,  # Simple placeholder
            "dimensions": 128,
            "input_token_count": len(text.split()),
            "text_length": len(text),
            "error": str(e),
            "warning": "Amazon Bedrock service unavailable, using simple placeholder",
        }


def batch_embed_platform_outputs(
    texts: List[str], model_id: str = "amazon.titan-embed-text-v2:0"
) -> List[Dict[str, Any]]:
    """Embed multiple platform outputs using Amazon Titan Embeddings."""

    bedrock_client = boto3.client(
        "bedrock-runtime",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    embeddings = []

    for i, text in enumerate(texts):
        try:
            # Prepare request for each text
            request_body = json.dumps(
                {"inputText": text, "dimensions": 1024, "normalize": True}
            )

            response = bedrock_client.invoke_model(
                modelId=model_id,
                contentType="application/json",
                accept="application/json",
                body=request_body,
            )

            response_body = json.loads(response["body"].read())
            embedding = response_body.get("embedding", [])

            embeddings.append(
                {
                    "provider": "amazon-bedrock",
                    "service": "TitanEmbeddings",
                    "model_id": model_id,
                    "embedding": embedding,
                    "dimensions": len(embedding),
                    "input_token_count": response_body.get("inputTextTokenCount", 0),
                    "text_length": len(text),
                    "item_index": i,
                    "success": True,
                }
            )

        except Exception as e:
            # Add error result for failed embeddings
            embeddings.append(
                {
                    "provider": "amazon-bedrock",
                    "service": "TitanEmbeddings",
                    "model_id": model_id,
                    "error": str(e),
                    "item_index": i,
                    "success": False,
                    "text_length": len(text),
                }
            )

    return embeddings


def get_available_embedding_models() -> List[Dict[str, str]]:
    """Get available embedding models from Amazon Bedrock."""

    bedrock_client = boto3.client(
        "bedrock",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    try:
        # List foundation models
        response = bedrock_client.list_foundation_models(byOutputModality="EMBEDDING")

        models = []
        for model_summary in response["modelSummaries"]:
            if "embed" in model_summary["modelName"].lower():
                models.append(
                    {
                        "model_id": model_summary["modelId"],
                        "model_name": model_summary["modelName"],
                        "provider_name": model_summary["providerName"],
                        "input_modalities": model_summary.get("inputModalities", []),
                        "output_modalities": model_summary.get("outputModalities", []),
                        "customizations_supported": model_summary.get(
                            "customizationsSupported", []
                        ),
                    }
                )

        return models

    except ClientError as e:
        print(f"Error listing embedding models: {e}")

        # Return default Titan embedding models
        return [
            {
                "model_id": "amazon.titan-embed-text-v2:0",
                "model_name": "Titan Embed Text v2",
                "provider_name": "Amazon",
                "input_modalities": ["TEXT"],
                "output_modalities": ["EMBEDDING"],
            },
            {
                "model_id": "amazon.titan-embed-text-v1:2:8k",
                "model_name": "Titan Embed Text v1",
                "provider_name": "Amazon",
                "input_modalities": ["TEXT"],
                "output_modalities": ["EMBEDDING"],
            },
        ]
