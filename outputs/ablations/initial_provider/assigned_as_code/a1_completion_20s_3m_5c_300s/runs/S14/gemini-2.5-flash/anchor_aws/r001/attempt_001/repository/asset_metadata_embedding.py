import json
from storage_client import get_bedrock_runtime_client
from storage_models import EmbeddingResult


def embed_asset_metadata_and_text(text: str, config: dict = None) -> EmbeddingResult:
    config = config or {}
    bedrock_runtime = get_bedrock_runtime_client(region_name=config.get("region"))
    model_id = "amazon.titan-embed-text-v1"
    body = json.dumps({"inputText": text})
    response = bedrock_runtime.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )
    response_body = json.loads(response.get('body').read())
    embedding = response_body.get('embedding')
    return EmbeddingResult(embedding=embedding)
