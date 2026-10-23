import boto3


def sign_or_verify_key(payload, config=None):
    config = config or {}
    client = boto3.client("kms", region_name=config.get("region"))
    if payload.get("signature"):
        response = client.verify(
            KeyId=config["key_id"],
            Message=payload["message"],
            Signature=payload["signature"],
            SigningAlgorithm=config.get("signing_algorithm", "RSASSA_PSS_SHA_256"),
        )
        return {"verified": response["SignatureValid"]}
    response = client.sign(
        KeyId=config["key_id"],
        Message=payload["message"],
        SigningAlgorithm=config.get("signing_algorithm", "RSASSA_PSS_SHA_256"),
    )
    return {"signature": response["Signature"]}
