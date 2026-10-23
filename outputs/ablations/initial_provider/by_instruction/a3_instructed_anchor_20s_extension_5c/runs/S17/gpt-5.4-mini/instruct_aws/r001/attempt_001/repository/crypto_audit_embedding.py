import boto3


def crypto_audit_embedding(note: str):
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=("{" + f'"inputText":"{note}"' + "}").encode("utf-8"),
        accept="application/json",
        contentType="application/json",
    )
    return {"provider": "aws-bedrock", "model": "amazon.titan-embed-text-v2:0", "response": response}
