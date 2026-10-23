import boto3
import json


def stream_platform_generation():
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
    for event in response.get("body"):
        yield json.loads(event)
