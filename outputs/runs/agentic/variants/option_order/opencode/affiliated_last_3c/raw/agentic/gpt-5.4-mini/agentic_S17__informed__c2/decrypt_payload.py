import base64

from security_client import create_vault_client, load_security_config
from security_models import DecryptionRequest, DecryptionResponse, normalize_text


def decrypt_payload(ciphertext: str, key_id: str | None = None) -> DecryptionResponse:
    cfg = load_security_config()
    client = create_vault_client()
    request = DecryptionRequest(
        ciphertext=normalize_text(ciphertext), key_id=key_id or cfg["vault_key_name"]
    )
    result = client.secrets.transit.decrypt_data(
        name=request.key_id,
        ciphertext=request.ciphertext,
        mount_point=cfg["vault_transit_mount"],
    )
    plaintext = base64.b64decode(result["data"]["plaintext"]).decode(
        "utf-8", errors="ignore"
    )
    return DecryptionResponse(plaintext=plaintext, key_id=request.key_id)
