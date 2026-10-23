import boto3

from security_models import decode_blob, normalize_payload


def sign_or_verify_key(payload, config=None):
    payload = normalize_payload(payload)
    config = config or {}
    client = boto3.client("kms", region_name=config.get("region"))
    if payload.get("signature"):
        response = client.verify(
            KeyId=config.get("signing_key_id") or config["key_id"],
            Message=payload["message"],
            MessageType="RAW",
            Signature=decode_blob(payload["signature"]),
            SigningAlgorithm=payload.get("signing_algorithm", "RSASSA_PSS_SHA_256"),
        )
        return {"verified": response["SignatureValid"]}
    response = client.sign(
        KeyId=config.get("signing_key_id") or config["key_id"],
        Message=payload["message"],
        MessageType="RAW",
        SigningAlgorithm=payload.get("signing_algorithm", "RSASSA_PSS_SHA_256"),
    )
    return {"signature": response["Signature"]}
