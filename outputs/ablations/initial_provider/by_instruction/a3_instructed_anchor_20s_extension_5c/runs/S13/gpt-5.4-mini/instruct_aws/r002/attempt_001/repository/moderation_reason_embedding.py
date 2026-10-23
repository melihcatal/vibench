import boto3


def moderation_reason_embedding(text):
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    body = '{"inputText": ' + __import__("json").dumps(text) + ', "modelId": "amazon.titan-embed-text-v2:0"}'
    response = client.invoke_model(modelId="amazon.titan-embed-text-v2:0", body=body, contentType="application/json", accept="application/json")
    payload = __import__("json").loads(response["body"].read())
    return {"provider": "aws", "embedding": payload.get("embedding", [])}
