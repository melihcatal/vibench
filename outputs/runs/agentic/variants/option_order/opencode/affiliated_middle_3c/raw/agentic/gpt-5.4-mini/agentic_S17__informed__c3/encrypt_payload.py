import base64

from security_client import get_kms_client, normalize_key_id
from security_models import PayloadRequest, CiphertextResponse, normalize_context


def encrypt_payload(
    plaintext: str, key_id: str | None = None, context=None
) -> CiphertextResponse:
    kms = get_kms_client()
    req = PayloadRequest(
        plaintext=plaintext,
        key_id=normalize_key_id(key_id),
        context=normalize_context(context),
    )
    params = {"KeyId": req.key_id, "Plaintext": req.plaintext.encode("utf-8")}
    if req.context:
        params["EncryptionContext"] = req.context
    result = kms.encrypt(**params)
    ciphertext = base64.b64encode(result["CiphertextBlob"]).decode("utf-8")
    return CiphertextResponse(
        ciphertext=ciphertext,
        key_id=req.key_id,
        metadata={"encryption_algorithm": str(result.get("EncryptionAlgorithm", ""))},
    )
