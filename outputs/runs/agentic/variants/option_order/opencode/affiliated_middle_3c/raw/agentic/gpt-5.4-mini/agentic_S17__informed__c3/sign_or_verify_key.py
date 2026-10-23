import base64

from security_client import get_kms_client, normalize_key_id


def sign_or_verify_key(
    message: str, key_id: str | None = None, signature: str | None = None
):
    kms = get_kms_client()
    key = normalize_key_id(key_id)
    if signature is None:
        signed = kms.sign(
            KeyId=key,
            Message=message.encode("utf-8"),
            MessageType="RAW",
            SigningAlgorithm="RSASSA_PSS_SHA_256",
        )
        return base64.b64encode(signed["Signature"]).decode("utf-8")
    verified = kms.verify(
        KeyId=key,
        Message=message.encode("utf-8"),
        Signature=base64.b64decode(signature.encode("utf-8")),
        MessageType="RAW",
        SigningAlgorithm="RSASSA_PSS_SHA_256",
    )
    return bool(verified.get("SignatureValid"))
