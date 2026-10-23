from security_client import kms_client, load_google_kms_config, crypto_key_path
from security_models import PayloadRequest, CiphertextResponse, normalize_text


def decrypt_payload(ciphertext: str, key_name: str, location: str = "global") -> str:
    config = load_google_kms_config()
    client = kms_client()
    request = PayloadRequest(plaintext=normalize_text(ciphertext), key_name=normalize_text(key_name), location=location)
    parent = crypto_key_path(config["project_id"], request.location or config["location"], config["key_ring"], request.key_name)
    response = client.decrypt(request={"name": parent, "ciphertext": request.plaintext.encode("latin1")})
    return response.plaintext.decode("utf-8")
