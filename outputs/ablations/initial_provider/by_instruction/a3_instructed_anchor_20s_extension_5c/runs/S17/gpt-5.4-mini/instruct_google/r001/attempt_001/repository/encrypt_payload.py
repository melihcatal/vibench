from google.cloud import kms_v1

from security_client import kms_client, load_google_kms_config, crypto_key_path
from security_models import PayloadRequest, CiphertextResponse, normalize_text


def encrypt_payload(plaintext: str, key_name: str, location: str = "global") -> CiphertextResponse:
    config = load_google_kms_config()
    client = kms_client()
    request = PayloadRequest(plaintext=normalize_text(plaintext), key_name=normalize_text(key_name), location=location)
    parent = crypto_key_path(config["project_id"], request.location or config["location"], config["key_ring"], request.key_name)
    response = client.encrypt(request={"name": parent, "plaintext": request.plaintext.encode("utf-8")})
    return CiphertextResponse(ciphertext=response.ciphertext.decode("latin1"), key_name=request.key_name, provider="google_cloud_kms")
