from security_client import get_secret_string, load_secret_id
from security_models import secret_version_request


def rotate_secret_version(version_stage: str | None = None, version_id: str | None = None):
    secret_id = load_secret_id("rotate/secret")
    request = secret_version_request(secret_id, version_stage, version_id)
    return {"request": request, "secret": get_secret_string(secret_id, version_stage=version_stage, version_id=version_id)}
