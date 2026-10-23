import base64

from security_client import create_kms_client, get_signing_key_id
from security_models import SignRequest, SignResponse


def sign_or_verify_key(message, key_id=None, signature=None):
    kms = create_kms_client()
    request = SignRequest.from_payload({"message": message, "key_id": key_id or get_signing_key_id()})
    if signature is None:
        result = kms.sign(KeyId=request.key_id, Message=request.message, MessageType="RAW", SigningAlgorithm="RSASSA_PSS_SHA_256")
        return SignResponse(signature=base64.b64encode(result["Signature"]).decode("utf-8"), verified=None, key_id=result["KeyId"]).to_payload()
    result = kms.verify(
        KeyId=request.key_id,
        Message=request.message,
        MessageType="RAW",
        Signature=base64.b64decode(signature.encode("utf-8")),
        SigningAlgorithm="RSASSA_PSS_SHA_256",
    )
    return SignResponse(signature=signature, verified=bool(result["SignatureValid"]), key_id=request.key_id).to_payload()
