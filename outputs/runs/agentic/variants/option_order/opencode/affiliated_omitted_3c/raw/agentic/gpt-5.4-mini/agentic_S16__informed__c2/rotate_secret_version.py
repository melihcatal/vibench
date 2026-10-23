import boto3
from security_client import get_secret_manager_client, resolve_secret_name
from security_models import RotationRequest


def rotate_secret_version() -> dict:
    request = RotationRequest(secret_id=resolve_secret_name("ROTATION_SECRET_ID", "app/rotating-secret"), version_stage="AWSCURRENT")
    client = get_secret_manager_client()
    response = client.get_secret_value(SecretId=request.secret_id, VersionStage=request.version_stage)
    payload = response.get("SecretString") or response.get("SecretBinary", b"").decode("utf-8")
    return {"secret_id": request.secret_id, "version_stage": request.version_stage, "value": payload}
