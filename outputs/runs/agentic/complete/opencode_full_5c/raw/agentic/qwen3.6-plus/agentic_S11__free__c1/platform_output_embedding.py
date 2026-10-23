from typing import Optional

from model_client import get_bedrock_runtime_client
from model_models import EmbeddingResult


BEDROCK_EMBEDDING_MODEL = "amazon.titan-embed-text-v2:0"


def embed_platform_output(
    text: str,
    model_id: Optional[str] = None,
    region: Optional[str] = None,
    input_type: Optional[str] = None,
) -> EmbeddingResult:
    target_model = model_id or BEDROCK_EMBEDDING_MODEL

    client = get_bedrock_runtime_client(region=region)

    body = {
        "inputText": text,
    }

    if "v2" in target_model and input_type:
        body["inputType"] = input_type

    response = client.invoke_model(
        modelId=target_model,
        body=__import__("json").dumps(body),
    )

    response_body = __import__("json").loads(response.get("body").read())

    embedding = response_body.get("embedding", [])
    input_tokens = response_body.get("inputTextTokenCount", 0)

    return EmbeddingResult(
        embedding=embedding,
        model_id=target_model,
        input_tokens=input_tokens,
        raw_response=response_body,
    )


def embed_multiple_platform_outputs(
    texts: list[str],
    model_id: Optional[str] = None,
    region: Optional[str] = None,
) -> list[EmbeddingResult]:
    results: list[EmbeddingResult] = []
    for text in texts:
        result = embed_platform_output(text, model_id=model_id, region=region)
        results.append(result)
    return results
