import boto3


def sign_or_verify_key(payload, config=None):
    config = config or {}
    kms = boto3.client("kms", region_name=config.get("region"))
    if payload.get("mode") == "sign":
        response = kms.sign(
            KeyId=config["key_id"],
            Message=payload["message"],
            MessageType="RAW",
            SigningAlgorithm=config.get("signing_algorithm", "RSASSA_PSS_SHA_256"),
        )
        return {"signature": response["Signature"]}
    response = kms.verify(
        KeyId=config["key_id"],
        Message=payload["message"],
        Signature=payload["signature"],
        MessageType="RAW",
        SigningAlgorithm=config.get("signing_algorithm", "RSASSA_PSS_SHA_256"),
    )
    return {"verified": response["SignatureValid"]}
