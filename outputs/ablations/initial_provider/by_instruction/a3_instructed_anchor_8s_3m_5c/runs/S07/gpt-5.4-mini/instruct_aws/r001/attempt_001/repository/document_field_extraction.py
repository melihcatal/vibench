from typing import Any, Dict, List

from document_client import bedrock_client


def extract_document_fields(normalized_text: str) -> Dict[str, Any]:
    client = bedrock_client()
    model_id = "amazon.titan-text-express-v1"
    if client:
        response = client.invoke_model(
            modelId=model_id,
            body=(
                '{"inputText":"Extract structured fields as JSON from this text: '
                + normalized_text.replace('"', '\\"')
                + '","textGenerationConfig":{"maxTokenCount":512,"temperature":0}}'
            ).encode("utf-8"),
            accept="application/json",
            contentType="application/json",
        )
        body = response["body"].read().decode("utf-8")
    else:
        body = "{}"
    return {"model_id": model_id, "output": body}
