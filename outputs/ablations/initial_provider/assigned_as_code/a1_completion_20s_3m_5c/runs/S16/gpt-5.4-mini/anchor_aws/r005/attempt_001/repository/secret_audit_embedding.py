import boto3

from security_client import load_config


def secret_audit_embedding(payload, config=None):
    config = load_config(config)
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    body = {"inputText": payload["notes"]}
    response = client.invoke_model(body=str(body).replace("'", '"'), modelId="amazon.titan-embed-text-v1", accept="application/json", contentType="application/json")
    return {"embedding": response["body"].read().decode("utf-8")}
