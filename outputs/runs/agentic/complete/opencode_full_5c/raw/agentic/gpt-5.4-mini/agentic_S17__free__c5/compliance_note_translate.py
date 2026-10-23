from security_client import SecurityClient


def compliance_note_translate(text: str, target_language: str = "es") -> dict:
    client = SecurityClient()
    prompt = f"Translate this compliance note to {target_language}: {text}"
    response = client.bedrock_runtime.invoke_model(
        modelId=client.bedrock_model_id(),
        body=('{"inputText": "' + prompt.replace('"', '\\"') + '"}').encode("utf-8"),
        contentType="application/json",
        accept="application/json",
    )
    return {
        "provider": "aws-bedrock-runtime",
        "model_id": client.bedrock_model_id(),
        "body": response["body"].read().decode("utf-8"),
    }
