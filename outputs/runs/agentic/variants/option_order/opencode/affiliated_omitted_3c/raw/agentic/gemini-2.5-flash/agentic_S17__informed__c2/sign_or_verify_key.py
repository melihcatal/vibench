from security_client import get_aws_kms_client
from security_models import SignRequest, SignResponse, VerifyRequest
import base64
import hashlib


def sign_payload(request: SignRequest) -> SignResponse:
    kms_client = get_aws_kms_client()

    # Hash the message before signing, as KMS expects a digest for certain algorithms
    message_digest = hashlib.sha256(request.message.encode("utf-8")).digest()

    response = kms_client.sign(
        KeyId=request.key_id,
        Message=message_digest,
        MessageType="DIGEST",
        SigningAlgorithm=request.signing_algorithm,
    )
    signature = base64.b64encode(response["Signature"]).decode("utf-8")
    return SignResponse(
        signature=signature,
        key_id=response["KeyId"],
        signing_algorithm=response["SigningAlgorithm"],
    )


def verify_payload(request: VerifyRequest) -> bool:
    kms_client = get_aws_kms_client()

    message_digest = hashlib.sha256(request.message.encode("utf-8")).digest()
    signature_blob = base64.b64decode(request.signature.encode("utf-8"))

    response = kms_client.verify(
        KeyId=request.key_id,
        Message=message_digest,
        MessageType="DIGEST",
        Signature=signature_blob,
        SigningAlgorithm=request.signing_algorithm,
    )
    return response["SignatureValid"]
