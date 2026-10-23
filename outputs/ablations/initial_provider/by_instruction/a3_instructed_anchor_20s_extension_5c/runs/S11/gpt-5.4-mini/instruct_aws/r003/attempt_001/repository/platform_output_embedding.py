import boto3


def platform_output_embedding(text: str):
    client = boto3.client("bedrock-runtime", region_name=(boto3.session.Session().region_name or "us-east-1"))
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        body='{"inputText": %s}' % __import__("json").dumps(text),
        accept="application/json",
        contentType="application/json",
    )
    raw = __import__("json").loads(response["body"].read())
    return {"embedding": raw.get("embedding", []), "raw": raw}
