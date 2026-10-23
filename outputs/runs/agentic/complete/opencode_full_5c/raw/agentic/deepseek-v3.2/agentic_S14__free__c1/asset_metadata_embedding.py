import boto3
import json
from typing import Dict, Any
from botocore.exceptions import ClientError
from storage_models import EmbeddingRequest, EmbeddingResponse


def embed_object_metadata_and_text(request: EmbeddingRequest) -> EmbeddingResponse:
    """Embed object metadata and extracted text for search using OpenAI via AWS Bedrock."""
    bedrock_runtime = boto3.client("bedrock-runtime")

    try:
        # Use Titan Embeddings model via AWS Bedrock
        response = bedrock_runtime.invoke_model(
            modelId="amazon.titan-embed-text-v1",
            contentType="application/json",
            accept="application/json",
            body=json.dumps({"inputText": request.text}),
        )

        response_body = json.loads(response["body"].read())
        embedding = response_body.get("embedding", [])

        if not embedding:
            # Fallback to OpenAI embeddings via AWS Bedrock (if configured)
            try:
                response = bedrock_runtime.invoke_model(
                    modelId="openai.gpt-3.5-turbo-instruct",
                    contentType="application/json",
                    accept="application/json",
                    body=json.dumps(
                        {
                            "prompt": f"Create embedding for: {request.text}",
                            "max_tokens": 0,
                            "embedding": True,
                        }
                    ),
                )
                response_body = json.loads(response["body"].read())
                embedding = response_body.get("embedding", [])
                model_used = "openai.gpt-3.5-turbo-instruct"
            except:
                # Use Cohere embeddings as another option
                response = bedrock_runtime.invoke_model(
                    modelId="cohere.embed-english-v3",
                    contentType="application/json",
                    accept="application/json",
                    body=json.dumps(
                        {"texts": [request.text], "input_type": "search_document"}
                    ),
                )
                response_body = json.loads(response["body"].read())
                embedding = response_body.get("embeddings", [[]])[0]
                model_used = "cohere.embed-english-v3"
        else:
            model_used = "amazon.titan-embed-text-v1"

        return EmbeddingResponse(
            success=True,
            embedding=embedding,
            model=model_used,
            dimensions=len(embedding) if embedding else 0,
            message=f"Embedding generated successfully using AWS Bedrock with {model_used} model",
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "ModelNotReadyException":
            return EmbeddingResponse(
                success=False,
                error_message="AWS Bedrock error: Embedding model not available or not ready",
            )
        elif error_code == "ValidationException":
            return EmbeddingResponse(
                success=False,
                error_message="AWS Bedrock error: Invalid text input for embedding",
            )
        return EmbeddingResponse(
            success=False, error_message=f"AWS Bedrock error: {str(e)}"
        )
    except Exception as e:
        return EmbeddingResponse(
            success=False, error_message=f"Embedding generation failed: {str(e)}"
        )


def create_combined_embedding(
    metadata: Dict[str, Any], extracted_text: str
) -> EmbeddingResponse:
    """Create embedding from combined metadata and text."""
    # Combine metadata and text for embedding
    combined_text = (
        f"Metadata: {json.dumps(metadata)}. Content: {extracted_text[:1000]}"
    )

    request = EmbeddingRequest(text=combined_text, model="amazon.titan-embed-text-v1")

    return embed_object_metadata_and_text(request)
