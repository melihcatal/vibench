import os

from security_client import fetch_secret, load_secret_request


def main():
    secret_id = os.environ["ROTATION_SECRET_ID"]
    version_stage = os.environ.get("SECRET_VERSION_STAGE")
    version_id = os.environ.get("SECRET_VERSION_ID")
    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    response = fetch_secret(load_secret_request(secret_id, version_stage=version_stage, version_id=version_id), region_name=region)
    print(response.secret_string)


if __name__ == "__main__":
    main()
