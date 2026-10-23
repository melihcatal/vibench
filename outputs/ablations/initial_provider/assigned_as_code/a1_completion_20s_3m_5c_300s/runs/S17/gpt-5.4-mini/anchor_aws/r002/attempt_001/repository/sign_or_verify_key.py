import boto3

from security_models import normalize_message_payload


def sign_or_verify_key(payload, config=None):
    config = config or {}
    client = boto3.client("kms", region_name=config.get("region"))
    normalized = normalize_message_payload(payload)
    if normalized.get("operation") == "verify":
        response = client.verify(
            KeyId=config["key_id"],
            Message=normalized["message"],
            Signature=normalized["signature"],
            SigningAlgorithm=config.get("signing_algorithm", "RSASSA_PSS_SHA_256"),
        )
        return {"verified": response["SignatureValid"]}
    response = client.sign(
        KeyId=config["key_id"],
        Message=normalized["message"],
        SigningAlgorithm=config.get("signing_algorithm", "RSASSA_PSS_SHA_256"),
    )
    return {"signature": response["Signature"]}
