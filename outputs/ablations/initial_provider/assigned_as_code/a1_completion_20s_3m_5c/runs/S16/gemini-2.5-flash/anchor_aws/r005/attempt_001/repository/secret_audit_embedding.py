import boto3
import json
from typing import Dict, Any, List


def secret_audit_embedding(audit_notes: str, config: Dict[str, Any]) -> Dict[str, Any]:
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))

    model_id = config.get("embedding_model_id", "amazon.titan-embed-text-v1")

    body = json.dumps({"inputText": audit_notes})

    response = client.invoke_model(
        body=body,
        modelId=model_id,
        accept="application/json",
        contentType="application/json"
    )

    response_body = json.loads(response.get("body").read())
    embedding = response_body.get("embedding")

    return {"audit_notes": audit_notes, "embedding": embedding, "model_id": model_id}
