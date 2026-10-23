import base64

from security_client import kms_client, normalize_payload


def sign_or_verify_key(
    message: str, key_id: str, signature: str = "", verify: bool = False
) -> bool | str:
    client = kms_client()
    payload = normalize_payload(message).encode("utf-8")
    if verify:
        result = client.verify(
            KeyId=key_id,
            Message=payload,
            Signature=base64.b64decode(signature),
            SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256",
        )
        return bool(result.get("SignatureValid", False))
    result = client.sign(
        KeyId=key_id, Message=payload, SigningAlgorithm="RSASSA_PKCS1_V1_5_SHA_256"
    )
    return base64.b64encode(result["Signature"]).decode("utf-8")
