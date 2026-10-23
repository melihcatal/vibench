import boto3


def embed_script(text: str) -> list[float]:
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    resp = client.invoke_model(modelId="amazon.titan-embed-text-v1", body=f'{{"inputText": {text!r}}}')
    payload = resp["body"].read().decode("utf-8")
    import json
    return json.loads(payload)["embedding"]
