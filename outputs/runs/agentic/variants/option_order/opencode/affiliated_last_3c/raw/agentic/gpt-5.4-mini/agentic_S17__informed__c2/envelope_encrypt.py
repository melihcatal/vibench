import base64

from security_client import create_vault_client, load_security_config
from security_models import EncryptionRequest, EncryptionResponse, normalize_text


def envelope_encrypt(plaintext: str, key_id: str | None = None) -> EncryptionResponse:
    cfg = load_security_config()
    client = create_vault_client()
    request = EncryptionRequest(
        plaintext=normalize_text(plaintext), key_id=key_id or cfg["vault_key_name"]
    )
    dek = client.secrets.transit.generate_data_key(
        name=request.key_id,
        key_type="plaintext",
        mount_point=cfg["vault_transit_mount"],
    )
    data_key = dek["data"]["plaintext_key"]
    wrapped_key = dek["data"]["ciphertext"]
    ciphertext = base64.b64encode(
        (request.plaintext + "|" + data_key).encode("utf-8")
    ).decode("ascii")
    return EncryptionResponse(
        ciphertext=ciphertext,
        key_id=request.key_id,
        metadata={"wrapped_key": wrapped_key},
    )
