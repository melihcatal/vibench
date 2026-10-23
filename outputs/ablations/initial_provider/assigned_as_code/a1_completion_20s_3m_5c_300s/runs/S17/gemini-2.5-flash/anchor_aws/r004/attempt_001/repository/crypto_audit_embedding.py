import boto3
import os
import json


def embed_audit_note(payload, config=None):
    config = config or {}
    region_name = config.get("region", os.environ.get("AWS_REGION"))
    if not region_name:
        raise ValueError("AWS region not provided in config or AWS_REGION environment variable.")

    bedrock_runtime_client = boto3.client("bedrock-runtime", region_name=region_name)

    audit_note = payload["audit_note"]
    model_id = config.get("bedrock_embedding_model_id", "amazon.titan-embed-text-v1")

    body = json.dumps({"inputText": audit_note})

    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response.get("body").read())
    embedding = response_body.get("embedding")

    return {"embedding": embedding}
