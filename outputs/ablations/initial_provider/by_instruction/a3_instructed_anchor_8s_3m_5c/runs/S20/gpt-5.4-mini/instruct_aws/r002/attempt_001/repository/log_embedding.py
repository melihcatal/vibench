import boto3


def log_embedding(text):
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=__import__("json").dumps({"inputText": text}),
        accept="application/json",
        contentType="application/json",
    )
    payload = __import__("json").loads(response["body"].read())
    return payload.get("embedding")
