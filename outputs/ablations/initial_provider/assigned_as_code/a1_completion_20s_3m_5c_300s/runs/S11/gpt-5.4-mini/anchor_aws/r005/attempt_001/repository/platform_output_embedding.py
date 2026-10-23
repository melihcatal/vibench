import boto3

from model_client import get_region


def platform_output_embedding(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=get_region(config))
    response = client.invoke_model(
        modelId=config.get("embedding_model_id", "amazon.titan-embed-text-v1"),
        body=("{" + f'"inputText":"{payload["text"].replace("\\", "\\\\").replace("\"", "\\\"")}"' + "}"),
        accept="application/json",
        contentType="application/json",
    )
    body = response["body"].read().decode("utf-8")
    return {"embedding_response": body, "response": response}
