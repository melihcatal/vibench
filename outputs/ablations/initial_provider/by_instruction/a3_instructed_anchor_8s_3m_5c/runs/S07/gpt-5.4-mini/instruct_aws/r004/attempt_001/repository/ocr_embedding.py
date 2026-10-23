from typing import Any, Dict

import boto3

from extract_text import extract_text


def embed_ocr_sections(document: Any, model_id: str = "amazon.titan-embed-text-v1") -> Dict[str, Any]:
    text = extract_text(document).text
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(
        modelId=model_id,
        body=("{\"inputText\": \"" + text.replace("\\", "\\\\").replace('"', '\\"') + "\"}").encode("utf-8"),
        accept="application/json",
        contentType="application/json",
    )
    return {"text": text, "embedding_response": response["body"].read().decode("utf-8")}
