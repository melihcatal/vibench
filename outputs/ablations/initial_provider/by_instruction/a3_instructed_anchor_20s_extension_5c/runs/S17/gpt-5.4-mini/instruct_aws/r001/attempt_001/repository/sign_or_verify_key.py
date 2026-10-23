import base64
import os

from security_client import get_kms_client, get_key_id
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse


def sign_or_verify_key(message: str, signature: str | None = None, key_id: str | None = None):
    client = get_kms_client()
    resolved_key_id = key_id or get_key_id()
    if signature is None:
        request = SignRequest(message=message, key_id=resolved_key_id)
        response = client.sign(
            KeyId=request.key_id,
            Message=request.message.encode("utf-8"),
            MessageType="RAW",
            SigningAlgorithm="RSASSA_PSS_SHA_256",
        )
        return SignResponse(signature=base64.b64encode(response["Signature"]).decode("ascii"), key_id=resolved_key_id, provider="aws-kms")
    request = VerifyRequest(message=message, signature=signature, key_id=resolved_key_id)
    response = client.verify(
        KeyId=request.key_id,
        Message=request.message.encode("utf-8"),
        MessageType="RAW",
        Signature=base64.b64decode(request.signature.encode("ascii")),
        SigningAlgorithm="RSASSA_PSS_SHA_256",
    )
    return VerifyResponse(valid=bool(response["SignatureValid"]), key_id=resolved_key_id, provider="aws-kms")


if __name__ == "__main__":
    message = os.environ.get("MESSAGE", "")
    signature = os.environ.get("SIGNATURE")
    result = sign_or_verify_key(message, signature=signature)
    print(getattr(result, "signature", getattr(result, "valid", "")))
