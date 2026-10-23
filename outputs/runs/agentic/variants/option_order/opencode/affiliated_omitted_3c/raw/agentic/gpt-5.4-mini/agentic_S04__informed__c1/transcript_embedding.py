import boto3


def transcript_embedding(text: str):
    client = boto3.client("bedrock-runtime")
    body = {"inputText": text}
    resp = client.invoke_model(modelId="amazon.titan-embed-text-v1", body=__import__("json").dumps(body), accept="application/json", contentType="application/json")
    return resp["body"].read().decode("utf-8")
