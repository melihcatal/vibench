from model_client import bedrock_runtime_client, model_id
from model_models import json_body


def platform_output_embedding(text: str):
    client = bedrock_runtime_client()
    response = client.invoke_model(
        modelId=model_id(),
        body=json_body({"inputText": text}),
        contentType="application/json",
        accept="application/json",
    )
    return response
