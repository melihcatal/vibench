import os

from security_client import load_secret
from security_models import SecretRequest


def rotate_secret_version():
    request = SecretRequest(secret_id=os.getenv("AWS_SECRET_ROTATION_ID", "rotation/secret"), version_stage=os.getenv("AWS_SECRET_ROTATION_STAGE") or "AWSPENDING", version_id=os.getenv("AWS_SECRET_ROTATION_VERSION_ID"))
    secret = load_secret(request)
    return {"secret_id": secret.secret_id, "version_id": secret.version_id, "version_stage": secret.version_stage, "payload": secret.payload}


if __name__ == "__main__":
    print(rotate_secret_version())
