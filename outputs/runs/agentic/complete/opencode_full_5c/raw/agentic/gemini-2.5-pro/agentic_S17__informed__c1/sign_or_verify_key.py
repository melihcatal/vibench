from security_client import get_kms_client
from security_models import SignPayload, VerifyPayload


def sign(payload: SignPayload) -> bytes:
    kms_client = get_kms_client()
    response = kms_client.sign(
        KeyId=payload.key_id,
        Message=payload.message,
        MessageType="RAW",
        SigningAlgorithm=payload.signing_algorithm,
    )
    return response["Signature"]


def verify(payload: VerifyPayload) -> bool:
    kms_client = get_kms_client()
    try:
        response = kms_client.verify(
            KeyId=payload.key_id,
            Message=payload.message,
            MessageType="RAW",
            Signature=payload.signature,
            SigningAlgorithm=payload.signing_algorithm,
        )
        return response["SignatureValid"]
    except Exception:
        return False
