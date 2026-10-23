import json
from datetime import datetime, timezone

from storage_client import get_bedrock_runtime_client
from storage_models import EmbeddingRequest, EmbeddingResponse, AssetEmbeddingRecord


def embed_object_metadata(
    object_key: str,
    bucket: str,
    metadata: dict = None,
    extracted_text: str = "",
    model_id: str = "amazon.titan-embed-text-v2:0",
) -> AssetEmbeddingRecord:
    bedrock_client = get_bedrock_runtime_client()

    metadata = metadata or {}

    metadata_parts = []
    for mk, mv in sorted(metadata.items()):
        metadata_parts.append(f"{mk}: {mv}")
    metadata_str = " | ".join(metadata_parts)

    if metadata_str and extracted_text:
        embedding_input = f"Metadata: {metadata_str}\n\nContent: {extracted_text}"
    elif metadata_str:
        embedding_input = f"Metadata: {metadata_str}"
    elif extracted_text:
        embedding_input = extracted_text
    else:
        embedding_input = object_key

    try:
        body = {
            "inputText": embedding_input,
            "dimensions": 1024,
            "normalize": True,
        }

        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=json.dumps(body),
        )

        response_body = json.loads(response.get("body").read())

        embedding_vector = response_body.get("embedding", [])
        input_tokens = response_body.get("inputTextTokenCount", 0)

        return AssetEmbeddingRecord(
            object_key=object_key,
            bucket=bucket,
            metadata=metadata,
            extracted_text=extracted_text,
            embedding=embedding_vector,
            embedding_model=model_id,
            created_at=datetime.now(timezone.utc),
        )

    except Exception as exc:
        return AssetEmbeddingRecord(
            object_key=object_key,
            bucket=bucket,
            metadata=metadata,
            extracted_text=extracted_text,
            embedding=[],
            embedding_model=model_id,
            created_at=datetime.now(timezone.utc),
        )


def generate_embedding(
    text: str,
    model_id: str = "amazon.titan-embed-text-v2:0",
) -> EmbeddingResponse:
    bedrock_client = get_bedrock_runtime_client()

    if not text or not text.strip():
        return EmbeddingResponse(
            success=False,
            error="Input text is empty",
        )

    try:
        body = {
            "inputText": text,
            "dimensions": 1024,
            "normalize": True,
        }

        response = bedrock_client.invoke_model(
            modelId=model_id,
            body=json.dumps(body),
        )

        response_body = json.loads(response.get("body").read())

        embedding_vector = response_body.get("embedding", [])
        input_tokens = response_body.get("inputTextTokenCount", 0)

        return EmbeddingResponse(
            success=True,
            embedding=embedding_vector,
            model_id=model_id,
            input_tokens=input_tokens,
        )

    except Exception as exc:
        return EmbeddingResponse(
            success=False,
            error=str(exc),
        )


def embed_from_request(request: EmbeddingRequest) -> EmbeddingResponse:
    return generate_embedding(
        text=request.text,
        model_id=request.model_id,
    )
