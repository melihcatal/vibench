import json
import os
from typing import List

from model_client import bedrock_runtime_client, model_id_for_task


def output_embedding(text: str) -> List[float]:
    client = bedrock_runtime_client()
    response = client.invoke_model(
        modelId=model_id_for_task("embed"),
        body=json.dumps({"inputText": text}).encode("utf-8"),
        accept="application/json",
        contentType="application/json",
    )
    raw = json.loads(response["body"].read())
    return raw.get("embedding", [])
