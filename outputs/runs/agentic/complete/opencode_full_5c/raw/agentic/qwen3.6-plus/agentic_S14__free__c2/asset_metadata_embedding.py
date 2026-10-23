import json

from storage_client import get_bedrock_runtime_client, handle_s3_error
from storage_models import EmbeddingRequest, EmbeddingResponse


def embed_object_metadata(
    text: str,
    model_id: str = "amazon.titan-embed-text-v2:0",
    dimensions: int = 1024,
    normalize: bool = True,
    region_name: str = None,
) -> EmbeddingResponse:
    bedrock = get_bedrock_runtime_client(region_name=region_name)
    body = json.dumps(
        {
            "inputText": text,
            "dimensions": dimensions,
            "normalize": normalize,
        }
    )
    try:
        response = bedrock.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=body,
        )
        response_body = json.loads(response.get("body").read())
        embedding = response_body.get("embedding", [])
        input_tokens = response_body.get("inputTextTokenCount", 0)
        return EmbeddingResponse(
            embedding=embedding,
            model_id=model_id,
            input_tokens=input_tokens,
        )
    except Exception as exc:
        error_code = (
            exc.response.get("Error", {}).get("Code", "Unknown")
            if hasattr(exc, "response")
            else "Unknown"
        )
        error_message = (
            exc.response.get("Error", {}).get("Message", str(exc))
            if hasattr(exc, "response")
            else str(exc)
        )
        raise RuntimeError(
            f"AWS Bedrock invoke_model (embedding) failed [{error_code}]: {error_message} "
            f"(model: {model_id})"
        ) from exc


def embed_from_request(
    request: EmbeddingRequest,
    region_name: str = None,
) -> EmbeddingResponse:
    return embed_object_metadata(
        text=request.text,
        model_id=request.model_id,
        dimensions=request.dimensions,
        normalize=request.normalize,
        region_name=region_name,
    )


def embed_combined_metadata(
    object_key: str,
    object_metadata: dict,
    extracted_text: str,
    model_id: str = "amazon.titan-embed-text-v2:0",
    dimensions: int = 1024,
    normalize: bool = True,
    region_name: str = None,
) -> EmbeddingResponse:
    meta_str = ", ".join(f"{k}={v}" for k, v in object_metadata.items())
    combined = (
        f"Object: {object_key} | Metadata: {meta_str} | Content: {extracted_text}"
    )
    return embed_object_metadata(
        text=combined,
        model_id=model_id,
        dimensions=dimensions,
        normalize=normalize,
        region_name=region_name,
    )
