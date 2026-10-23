import base64

from security_client import kms_client, load_config


def sign_or_verify_key(message: str, signature: str | None = None) -> dict:
    config = load_config()
    client = kms_client(config)
    if signature is None:
        response = client.sign(
            KeyId=config.signing_key_id,
            Message=message.encode("utf-8"),
            MessageType="RAW",
            SigningAlgorithm="RSASSA_PSS_SHA_256",
        )
        return {
            "key_id": config.signing_key_id,
            "signature": base64.b64encode(response["Signature"]).decode("utf-8"),
        }
    response = client.verify(
        KeyId=config.signing_key_id,
        Message=message.encode("utf-8"),
        Signature=base64.b64decode(signature.encode("utf-8")),
        MessageType="RAW",
        SigningAlgorithm="RSASSA_PSS_SHA_256",
    )
    return {
        "key_id": config.signing_key_id,
        "verified": bool(response["SignatureValid"]),
    }
