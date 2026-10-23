import json

import boto3


def secret_audit_embedding(payload, config=None):
    config = config or {}
    bedrock_runtime_client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    
    model_id = "amazon.titan-embed-text-v1"
    text_to_embed = payload["audit_notes"]
    
    body = json.dumps({"inputText": text_to_embed})
    
    response = bedrock_runtime_client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )
    
    response_body = json.loads(response.get("body").read())
    embedding = response_body.get("embedding")
    
    return {"secret_id": payload["secret_id"], "embedding": embedding}
