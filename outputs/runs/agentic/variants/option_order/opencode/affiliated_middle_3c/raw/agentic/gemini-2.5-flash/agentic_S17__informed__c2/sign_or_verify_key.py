import base64
from security_client import security_client
from security_models import SignRequest, SignResponse, VerifyRequest, VerifyResponse


def sign_message(request: SignRequest) -> SignResponse:
    message_bytes = request.message.encode("utf-8")
    response = security_client.kms_client.sign(
        KeyId=request.key_id,
        Message=message_bytes,
        MessageType="RAW",
        SigningAlgorithm=request.signing_algorithm,
    )
    signature = response["Signature"]
    return SignResponse(
        signature=signature,
        key_id=request.key_id,
        signing_algorithm=request.signing_algorithm,
    )


def verify_signature(request: VerifyRequest) -> VerifyResponse:
    message_bytes = request.message.encode("utf-8")
    response = security_client.kms_client.verify(
        KeyId=request.key_id,
        Message=message_bytes,
        MessageType="RAW",
        Signature=request.signature,
        SigningAlgorithm=request.signing_algorithm,
    )
    signature_valid = response["SignatureValid"]
    return VerifyResponse(signature_valid=signature_valid, key_id=request.key_id)
