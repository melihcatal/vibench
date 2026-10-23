from typing import Any, Dict, List

import boto3


def summarize_message_processing(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    prompt = "Summarize message processing results: " + str(results)
    return {"provider": "amazon-bedrock", "model_id": "amazon.nova-lite-v1:0", "prompt": prompt, "client": client.meta.service_model.service_name}
