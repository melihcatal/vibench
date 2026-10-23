import base64

from security_client import create_vault_client, load_security_config
from security_models import EncryptionRequest, EncryptionResponse, normalize_text


def encrypt_payload(plaintext: str, key_id: str | None = None) -> EncryptionResponse:
    cfg = load_security_config()
    client = create_vault_client()
    request = EncryptionRequest(
        plaintext=normalize_text(plaintext), key_id=key_id or cfg["vault_key_name"]
    )
    result = client.secrets.transit.encrypt_data(
        name=request.key_id,
        plaintext=base64.b64encode(request.plaintext.encode("utf-8")).decode("ascii"),
        mount_point=cfg["vault_transit_mount"],
    )
    return EncryptionResponse(
        ciphertext=result["data"]["ciphertext"],
        key_id=request.key_id,
        metadata=result.get("data"),
    )
