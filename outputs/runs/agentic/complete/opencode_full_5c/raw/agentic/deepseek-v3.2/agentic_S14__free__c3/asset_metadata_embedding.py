import boto3
import os
import json
from typing import Dict, Any
from storage_models import EmbeddingRequest, EmbeddingResponse


def embed_asset_metadata(request: EmbeddingRequest) -> EmbeddingResponse:
    """
    Embed object metadata and extracted text for search using Amazon Bedrock Titan embeddings.
    """
    try:
        # Initialize Amazon Bedrock client
        bedrock_client = boto3.client(
            "bedrock-runtime",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

        # Use Amazon Titan Embeddings model
        model_id = "amazon.titan-embed-text-v2:0"

        # Prepare the embedding request
        body = json.dumps(
            {
                "inputText": request.text,
                "dimensions": 1024,  # Titan v2 supports configurable dimensions
            }
        )

        # Call Amazon Bedrock for embeddings
        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=body,
            contentType="application/json",
            accept="application/json",
        )

        # Parse the response
        response_body = json.loads(response["body"].read())
        embedding = response_body.get("embedding")

        if not embedding:
            raise ValueError("No embedding returned from Amazon Titan model")

        return EmbeddingResponse(
            success=True,
            embedding=embedding,
            model=model_id,
            dimensions=len(embedding),
            message=f"Embedding generated using Amazon Bedrock Titan model",
        )

    except Exception as e:
        return EmbeddingResponse(
            success=False,
            error_message=str(e),
            message=f"Embedding failed using Amazon Bedrock: {e}",
        )
