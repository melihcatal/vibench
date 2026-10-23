import boto3
from botocore.exceptions import ClientError
import json
from storage_models import EmbeddingRequest, EmbeddingResponse
from typing import Dict, Any


def embed_asset_metadata(request: EmbeddingRequest) -> EmbeddingResponse:
    """
    Embed object metadata and extracted text for search using OpenAI via AWS Bedrock.
    """
    try:
        # Create Bedrock runtime client
        bedrock_client = boto3.client("bedrock-runtime")

        # Prepare the text for embedding
        text_to_embed = request.text

        # Call AWS Bedrock with Titan Embeddings model
        response = bedrock_client.invoke_model(
            modelId="amazon.titan-embed-text-v1",
            contentType="application/json",
            accept="application/json",
            body=json.dumps({"inputText": text_to_embed}),
        )

        # Parse response
        response_body = json.loads(response["body"].read())
        embedding = response_body.get("embedding", [])

        if not embedding:
            return EmbeddingResponse(
                success=False,
                text=request.text,
                error_message="AWS Bedrock Titan Embeddings returned empty embedding",
            )

        return EmbeddingResponse(
            success=True,
            text=request.text,
            embedding=embedding,
            model="amazon.titan-embed-text-v1",
            message=f"Embedding generated using AWS Bedrock Titan Embeddings model",
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ValidationException":
            return EmbeddingResponse(
                success=False,
                text=request.text,
                error_message=f"AWS Bedrock error: Validation failed - {str(e)}",
            )
        elif error_code == "ModelErrorException":
            return EmbeddingResponse(
                success=False,
                text=request.text,
                error_message=f"AWS Bedrock error: Model error - {str(e)}",
            )
        elif error_code == "ThrottlingException":
            return EmbeddingResponse(
                success=False,
                text=request.text,
                error_message=f"AWS Bedrock error: Rate limit exceeded - {str(e)}",
            )
        else:
            return EmbeddingResponse(
                success=False,
                text=request.text,
                error_message=f"AWS Bedrock error: {str(e)}",
            )
    except Exception as e:
        return EmbeddingResponse(
            success=False,
            text=request.text,
            error_message=f"Embedding generation error: {str(e)}",
        )


def create_combined_embedding(
    metadata: Dict[str, Any], extracted_text: str
) -> EmbeddingResponse:
    """
    Create embedding from combined metadata and extracted text.
    """
    # Combine metadata and text into a single string for embedding
    combined_text = f"Metadata: {json.dumps(metadata)}. Content: {extracted_text}"

    # Truncate if too long (Titan has limits)
    max_length = 8000
    if len(combined_text) > max_length:
        combined_text = combined_text[:max_length]

    # Create embedding request
    embedding_request = EmbeddingRequest(
        text=combined_text, model="amazon.titan-embed-text-v1"
    )

    # Generate embedding
    return embed_asset_metadata(embedding_request)
