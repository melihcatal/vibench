import boto3


def invoke_platform_model():
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
    return json.loads(response.get("body").read())
