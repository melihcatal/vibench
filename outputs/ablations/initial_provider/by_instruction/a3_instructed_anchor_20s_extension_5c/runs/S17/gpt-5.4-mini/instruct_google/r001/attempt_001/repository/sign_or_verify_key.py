from google.cloud import kms_v1

from security_client import kms_client, load_google_kms_config, key_version_path
from security_models import SignedPayload, normalize_text


def sign_or_verify_key(payload: str, key_name: str, location: str = "global", verify_signature: str = "") -> SignedPayload:
    config = load_google_kms_config()
    client = kms_client()
    name = key_version_path(config["project_id"], location or config["location"], config["key_ring"], normalize_text(key_name))
    if verify_signature:
        client.verify_integrity(request={"name": name, "data": normalize_text(payload).encode("utf-8"), "signature": normalize_text(verify_signature).encode("latin1")})
        signature = verify_signature
    else:
        signature = client.asymmetric_sign(request={"name": name, "digest": {"sha256": __import__("hashlib").sha256(normalize_text(payload).encode("utf-8")).digest()}}).signature.decode("latin1")
    return SignedPayload(payload=normalize_text(payload), signature=signature, key_name=normalize_text(key_name), provider="google_cloud_kms")
