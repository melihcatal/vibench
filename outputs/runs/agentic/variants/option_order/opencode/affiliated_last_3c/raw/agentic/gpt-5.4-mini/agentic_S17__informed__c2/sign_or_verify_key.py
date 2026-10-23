from security_client import create_vault_client, load_security_config
from security_models import SignRequest, SignResponse, normalize_text


def sign_or_verify_key(message: str, key_id: str | None = None) -> SignResponse:
    cfg = load_security_config()
    client = create_vault_client()
    request = SignRequest(
        message=normalize_text(message), key_id=key_id or cfg["vault_key_name"]
    )
    result = client.secrets.transit.sign_data(
        name=request.key_id,
        input=request.message.encode("utf-8").hex(),
        prehashed=False,
        hash_algorithm="sha2-256",
        mount_point=cfg["vault_transit_mount"],
    )
    return SignResponse(signature=result["data"]["signature"], key_id=request.key_id)
