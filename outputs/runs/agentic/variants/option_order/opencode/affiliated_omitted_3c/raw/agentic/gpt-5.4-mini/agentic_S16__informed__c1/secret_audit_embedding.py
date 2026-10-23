import boto3


def secret_audit_embedding(notes: str) -> list:
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v1",
        body=('{"inputText": "' + notes.replace('"', '\\"') + '"}').encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )
    return response["body"].read()
