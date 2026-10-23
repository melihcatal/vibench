from typing import Dict, List

import boto3


def image_summary(labels: List[Dict[str, object]], text_items: List[Dict[str, object]]) -> Dict[str, str]:
    client = boto3.client("bedrock-runtime")
    label_names = [str(item.get("name") or item.get("text") or "") for item in labels if item]
    text_values = [str(item.get("text") or "") for item in text_items if item]
    prompt = "Summarize this image analysis in one sentence. Labels: " + ", ".join(label_names) + ". Text: " + ", ".join(text_values)
    body = {"inputText": prompt, "textGenerationConfig": {"maxTokenCount": 80, "temperature": 0.2, "topP": 0.9}}
    response = client.invoke_model(modelId="anthropic.claude-3-haiku-20240307-v1:0", body=str(body).encode("utf-8"), contentType="application/json", accept="application/json")
    return {"provider": "aws.bedrock-runtime", "model_id": "anthropic.claude-3-haiku-20240307-v1:0", "raw": str(response)}
