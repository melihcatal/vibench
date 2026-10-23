from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class EmbeddingRequest:
    texts: List[str]
    model: Optional[str] = None
    input_type: Optional[str] = None  # For providers like Cohere


@dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]
    model: Optional[str] = None
    usage: Optional[Dict[str, Any]] = None


def normalize_embedding_response(raw_response: Any, provider: str) -> EmbeddingResponse:
    """
    Normalizes raw responses from different embedding providers into a common EmbeddingResponse format.
    """
    embeddings: List[List[float]] = []
    model_id: Optional[str] = None
    usage: Dict[str, Any] = {}

    if provider == "dashscope":
        if (
            raw_response.status_code == 200
            and raw_response.output
            and raw_response.output.embeddings
        ):
            embeddings = [item.embedding for item in raw_response.output.embeddings]
            model_id = raw_response.output.model_id
            usage = {"total_tokens": raw_response.usage.total_tokens}
        else:
            raise ValueError(f"Invalid DashScope response: {raw_response.message}")
    elif provider == "bedrock-titan":
        response_body = json.loads(raw_response.get("body").read())
        embeddings = [item["embedding"] for item in response_body.get("embeddings", [])]
        model_id = raw_response.get(
            "modelId"
        )  # Bedrock runtime does not return modelId in body
        usage = {"prompt_token_count": response_body.get("inputTextTokenCount")}
    elif provider == "openai":
        embeddings = [data.embedding for data in raw_response.data]
        model_id = raw_response.model
        usage = raw_response.usage.model_dump() if raw_response.usage else {}
    elif provider == "cohere":
        embeddings = raw_response.embeddings
        model_id = (
            raw_response.meta.api_version.version
            if raw_response.meta and raw_response.meta.api_version
            else None
        )  # Cohere response doesn't directly give model name here
        usage = {
            "prompt_token_count": raw_response.meta.tokens.input_tokens
            if raw_response.meta and raw_response.meta.tokens
            else 0
        }
    else:
        raise ValueError(f"Normalization not implemented for provider: {provider}")

    return EmbeddingResponse(embeddings=embeddings, model=model_id, usage=usage)


import json  # Required for json.loads
