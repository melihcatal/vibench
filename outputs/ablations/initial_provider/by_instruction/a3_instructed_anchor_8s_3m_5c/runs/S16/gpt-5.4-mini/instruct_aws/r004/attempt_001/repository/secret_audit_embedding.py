import boto3


def embed_audit_notes(text: str):
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=("{" + f'"inputText":"{text.replace("\\", "\\\\").replace("\"", "\\\"")}"' + "}").encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )
    return response["body"].read()
