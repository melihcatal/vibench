import json

from document_client import bedrock_runtime_client


def extract_document_fields(normalized_text: str) -> dict:
    client = bedrock_runtime_client()
    body = json.dumps({"inputText": normalized_text})
    response = client.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=body,
        contentType="application/json",
        accept="application/json",
    )
    payload = response["body"].read().decode("utf-8")
    return {"raw": payload}
