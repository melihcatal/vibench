import boto3

from security_client import load_security_client_config


def crypto_audit_embedding(text: str) -> dict:
    bedrock = boto3.client("bedrock-runtime", region_name=load_security_client_config().region_name)
    return bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=text.encode("utf-8"),
        accept="application/json",
        contentType="application/json",
    )


def main() -> None:
    crypto_audit_embedding("sample audit note")


if __name__ == "__main__":
    main()
