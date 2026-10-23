import boto3


def platform_output_embedding(text: str, model_id: str = "amazon.titan-embed-text-v1"):
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(modelId=model_id, body=("{\"inputText\": \"" + text.replace("\\", "\\\\").replace('"', '\\"') + "\"}"))
    return response["body"].read().decode("utf-8")
