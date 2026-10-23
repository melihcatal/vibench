from __future__ import annotations

from typing import Any, Dict

import boto3

from model_client import load_config



def platform_output_embedding(text: str) -> Dict[str, Any]:
    config = load_config()
    client = boto3.client("bedrock-runtime", region_name=config.aws_region)
    response = client.invoke_model(
        modelId=config.embedding_model_id,
        body=__import__("json").dumps({"inputText": text}),
        contentType="application/json",
        accept="application/json",
    )
    payload = __import__("json").loads(response["body"].read())
    return {"provider": "Amazon Bedrock", "model_id": config.embedding_model_id, "embedding": payload}
