import json
from security_client import build_secrets_client, normalize_secret_name
from security_models import SecretRequest, ParsedJsonSecret


def parse_json_secret(secret_id: str, version_stage: str = "AWSCURRENT") -> ParsedJsonSecret:
    client = build_secrets_client()
    request = SecretRequest(secret_id=secret_id, version_stage=version_stage)
    response = client.get_secret_value(SecretId=normalize_secret_name(request.secret_id), VersionStage=request.version_stage)
    payload = response.get("SecretString") or response["SecretBinary"].decode("utf-8")
    return ParsedJsonSecret.from_json(payload)
