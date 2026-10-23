import json
import os

import boto3


def read_secret_version(secret_id: str | None = None, version_id: str | None = None, version_stage: str | None = None) -> str:
    secret_name = secret_id or os.environ.get("AWS_SECRETS_MANAGER_SECRET_ID")
    if not secret_name:
        raise ValueError("AWS_SECRETS_MANAGER_SECRET_ID is required")

    region = os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION")
    client_kwargs = {}
    if region:
        client_kwargs["region_name"] = region

    client = boto3.client("secretsmanager", **client_kwargs)
    get_kwargs = {"SecretId": secret_name}
    if version_id:
        get_kwargs["VersionId"] = version_id
    if version_stage:
        get_kwargs["VersionStage"] = version_stage

    response = client.get_secret_value(**get_kwargs)
    if response.get("SecretString") is not None:
        return response["SecretString"]

    secret_binary = response.get("SecretBinary")
    if secret_binary is not None:
        return secret_binary.decode("utf-8")

    raise RuntimeError("Secret value was empty")


def read_staged_secret_value(secret_id: str | None = None, stage: str = "AWSCURRENT") -> str:
    return read_secret_version(secret_id=secret_id, version_stage=stage)


def main() -> None:
    secret_id = os.environ.get("AWS_SECRETS_MANAGER_SECRET_ID")
    version_id = os.environ.get("AWS_SECRETS_MANAGER_VERSION_ID")
    version_stage = os.environ.get("AWS_SECRETS_MANAGER_VERSION_STAGE")
    staged_only = os.environ.get("AWS_SECRETS_MANAGER_READ_STAGE_ONLY") == "1"

    if staged_only:
        value = read_staged_secret_value(secret_id=secret_id, stage=version_stage or "AWSCURRENT")
    else:
        value = read_secret_version(secret_id=secret_id, version_id=version_id, version_stage=version_stage)

    print(value)


if __name__ == "__main__":
    main()
