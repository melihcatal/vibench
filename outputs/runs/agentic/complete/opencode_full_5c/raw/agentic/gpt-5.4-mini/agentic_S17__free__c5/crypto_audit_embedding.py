from security_client import SecurityClient


def crypto_audit_embedding(text: str) -> dict:
    client = SecurityClient()
    response = client.bedrock_runtime.invoke_model(
        modelId=client.bedrock_model_id(),
        body=('{"inputText": "' + text.replace('"', '\\"') + '"}').encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )
    return {
        "provider": "aws-bedrock-runtime",
        "model_id": client.bedrock_model_id(),
        "body": response["body"].read().decode("utf-8"),
    }
