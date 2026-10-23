from security_client import SecurityClient


def payload_safety(text: str) -> dict:
    client = SecurityClient()
    lowered = text.lower()
    unsafe = any(
        token in lowered for token in ["rm -rf", "drop table", "<script", "secret="]
    )
    return {
        "safe": not unsafe,
        "provider": "aws-bedrock-runtime",
        "model_id": client.bedrock_model_id(),
    }
