import boto3
import json
from botocore.exceptions import ClientError
from typing import Dict, Any
from storage_models import EmbeddingRequest, EmbeddingResponse


def embed_metadata_and_text(request: EmbeddingRequest) -> EmbeddingResponse:
    """Embed object metadata and extracted text for search using AWS Bedrock Titan embeddings."""

    try:
        # Initialize AWS Bedrock runtime client
        bedrock_client = boto3.client(
            "bedrock-runtime",
            region_name="us-east-1",
            aws_access_key_id=boto3.Session().get_credentials().access_key,
            aws_secret_access_key=boto3.Session().get_credentials().secret_key,
        )

        # Use AWS Titan Embeddings model
        model_id = "amazon.titan-embed-text-v1"

        # Prepare request for Titan embeddings
        response = bedrock_client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps({"inputText": request.text}),
        )

        # Parse response
        response_body = json.loads(response["body"].read())
        embedding = response_body.get("embedding", [])

        return EmbeddingResponse(
            success=True,
            embedding=embedding,
            model=model_id,
            dimensions=len(embedding),
            message=f"Successfully generated embeddings using AWS Bedrock Titan model",
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"] if "Error" in e.response else "Unknown"
        return EmbeddingResponse(
            success=False,
            error_message=str(e),
            message=f"AWS Bedrock embedding failed: {error_code}",
        )
    except Exception as e:
        return EmbeddingResponse(
            success=False,
            error_message=str(e),
            message=f"Embedding generation failed: {str(e)}",
        )


def create_combined_embedding(
    metadata: Dict[str, Any], extracted_text: str
) -> EmbeddingResponse:
    """Create embedding from combined metadata and text."""

    # Combine metadata and text into a single string for embedding
    combined_text = f"Metadata: {json.dumps(metadata)}\n\nContent: {extracted_text}"

    request = EmbeddingRequest(text=combined_text, model="amazon.titan-embed-text-v1")

    return embed_metadata_and_text(request)
