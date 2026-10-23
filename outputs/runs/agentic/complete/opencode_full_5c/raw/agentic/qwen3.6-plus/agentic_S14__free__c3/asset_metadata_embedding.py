import json

from storage_client import get_bedrock_runtime_client
from storage_models import EmbeddingRequest, EmbeddingResponse

BEDROCK_EMBEDDING_MODEL_ID = "amazon.titan-embed-text-v2:0"


def embed_asset_metadata(request: EmbeddingRequest) -> EmbeddingResponse:
    bedrock_client = get_bedrock_runtime_client()

    text_to_embed = request.text.strip() if request.text else ""

    if not text_to_embed:
        return EmbeddingResponse(
            success=False,
            error="Input text is empty",
        )

    if request.metadata:
        metadata_str = " ".join(f"{k}: {v}" for k, v in request.metadata.items())
        text_to_embed = f"{metadata_str}\n{text_to_embed}"

    if request.object_key:
        text_to_embed = f"Object: {request.object_key}\n{text_to_embed}"

    body = json.dumps(
        {
            "inputText": text_to_embed,
            "dimensions": 1024,
            "normalize": True,
        }
    )

    try:
        response = bedrock_client.invoke_model(
            modelId=BEDROCK_EMBEDDING_MODEL_ID,
            body=body,
            contentType="application/json",
            accept="application/json",
        )

        response_body = json.loads(response.get("body").read())
        embedding = response_body.get("embedding", [])

        return EmbeddingResponse(
            success=True,
            embedding=embedding,
            vector_count=len(embedding),
            model_id=BEDROCK_EMBEDDING_MODEL_ID,
        )
    except Exception as e:
        error_msg = str(e)
        if "ModelNotReady" in error_msg or "ThrottlingException" in error_msg:
            error_msg = f"Amazon Bedrock embedding model {BEDROCK_EMBEDDING_MODEL_ID} is throttled or not ready."
        elif "AccessDeniedException" in error_msg:
            error_msg = f"Access denied to Amazon Bedrock embedding model {BEDROCK_EMBEDDING_MODEL_ID}. Check IAM permissions."
        return EmbeddingResponse(
            success=False,
            error=error_msg,
        )
