import boto3
import json


def collect_platform_metadata():
    client = boto3.client("bedrock-runtime")
    model_id = "amazon.titan-text-express-v1"
    body = {
        "inputText": "Translate this to German: Hello, how are you?",
        "textGenerationConfig": {"maxTokenCount": 1024, "temperature": 0, "topP": 0.9},
    }
    response = client.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )
    result = json.loads(response.get("body").read())
    metadata = {"model_id": model_id, "usage": response.get("usage")}
    return result, metadata
