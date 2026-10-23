import json

from security_client import get_default_key_id, get_kms_client
from security_models import OperationResult, normalize_text


def sign_or_verify_key(message, signature=None, key_id=None):
    client = get_kms_client()
    resolved_key_id = key_id or get_default_key_id()
    if signature is None:
        response = client.sign(
            KeyId=resolved_key_id,
            Message=normalize_text(message).encode("utf-8"),
            MessageType="RAW",
            SigningAlgorithm="RSASSA_PSS_SHA_256",
        )
        return OperationResult(
            ok=True,
            data={
                "signature_b64": response["Signature"].hex(),
                "key_id": resolved_key_id,
                "mode": "sign",
            },
        )
    response = client.verify(
        KeyId=resolved_key_id,
        Message=normalize_text(message).encode("utf-8"),
        MessageType="RAW",
        Signature=bytes.fromhex(signature),
        SigningAlgorithm="RSASSA_PSS_SHA_256",
    )
    return OperationResult(
        ok=True,
        data={
            "verified": bool(response["SignatureValid"]),
            "key_id": resolved_key_id,
            "mode": "verify",
        },
    )


def main():
    print(json.dumps(sign_or_verify_key("sample").data))


if __name__ == "__main__":
    main()
