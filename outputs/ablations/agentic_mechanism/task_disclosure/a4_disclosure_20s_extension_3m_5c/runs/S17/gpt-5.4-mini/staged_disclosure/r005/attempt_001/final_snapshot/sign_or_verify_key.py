from google.cloud import kms_v1
import base64
import hashlib
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa


def sign_or_verify_key(message: bytes, key_name: str, purpose: str, signature_b64: str | None = None):
    client = kms_v1.KeyManagementServiceClient()
    if purpose == "sign":
        response = client.asymmetric_sign(
            request={"name": key_name, "digest": {"sha256": hashlib.sha256(message).digest()}}
        )
        return response.signature
    if purpose == "verify":
        if signature_b64 is None:
            raise ValueError("signature_b64 is required for verification")
        signature = base64.b64decode(signature_b64)
        public_key_pem = client.get_public_key(name=key_name).pem
        public_key = serialization.load_pem_public_key(public_key_pem.encode())
        try:
            if isinstance(public_key, rsa.RSAPublicKey):
                public_key.verify(signature, message, padding.PKCS1v15(), hashes.SHA256())
            elif isinstance(public_key, ec.EllipticCurvePublicKey):
                public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
            else:
                raise ValueError("Unsupported public key type")
            return True
        except Exception:
            return False
    raise ValueError("purpose must be 'sign' or 'verify'")
