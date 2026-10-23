from typing import Any, Dict

from document_client import bedrock_client


def embed_ocr_sections(text: str) -> Dict[str, Any]:
    client = bedrock_client()
    model_id = "amazon.titan-embed-text-v2:0"
    if client:
        response = client.invoke_model(
            modelId=model_id,
            body=(f'{{"inputText":"{text.replace("\"", "\\\"")}"}}').encode("utf-8"),
            accept="application/json",
            contentType="application/json",
        )
        output = response["body"].read().decode("utf-8")
    else:
        output = "{}"
    return {"model_id": model_id, "embedding": output}
