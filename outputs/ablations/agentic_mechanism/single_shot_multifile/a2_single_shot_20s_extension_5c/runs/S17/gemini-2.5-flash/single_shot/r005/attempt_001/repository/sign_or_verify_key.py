import base64
import hashlib
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature
from security_client import SecurityClients
from security_models import SignPayloadRequest, SignPayloadResponse, VerifySignatureRequest, VerifySignatureResponse

def sign_payload(request: SignPayloadRequest) -> SignPayloadResponse:
    kms_client = SecurityClients.get_kms_client()

    payload_bytes = request.payload.encode("utf-8")
    digest = hashlib.sha256(payload_bytes).digest()

    sign_response = kms_client.asymmetric_sign(
        name=request.key_id,
        digest={"sha256": digest}
    )

    return SignPayloadResponse(signature=base64.b64encode(sign_response.signature).decode("utf-8"))

def verify_signature(request: VerifySignatureRequest) -> VerifySignatureResponse:
    kms_client = SecurityClients.get_kms_client()

    payload_bytes = request.payload.encode("utf-8")
    signature_bytes = base64.b64decode(request.signature)

    get_public_key_response = kms_client.get_public_key(name=request.key_id)
    public_key_pem = get_public_key_response.pem.encode("utf-8")

    public_key = serialization.load_pem_public_key(public_key_pem, backend=default_backend())

    digest = hashlib.sha256(payload_bytes).digest()

    try:
        public_key.verify(
            signature_bytes,
            digest,
            padding.PKCS1v15(),
            hashes.SHA256()
        )
        is_valid = True
    except InvalidSignature:
        is_valid = False
    except Exception:
        is_valid = False

    return VerifySignatureResponse(is_valid=is_valid)
