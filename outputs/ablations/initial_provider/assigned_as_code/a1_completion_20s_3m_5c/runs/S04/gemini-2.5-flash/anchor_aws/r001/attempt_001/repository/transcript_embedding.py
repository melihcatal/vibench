import json
from typing import Dict, Any, List

from speech_client import get_bedrock_runtime_client
from speech_models import normalize_embedding_result

def embed_transcript(text_segment: str, config: Dict[str, Any] = None) -> List[float]:
    config = config or {}
    client = get_bedrock_runtime_client(region_name=config.get("region"))

    # Using Amazon Titan Embeddings G1 - Text as an example model
    model_id = config.get("bedrock_embedding_model_id", "amazon.titan-embed-text-v1")

    body = json.dumps({"inputText": text_segment})

    response = client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response.get("body").read())
    return normalize_embedding_result(response_body)
