import os
from typing import Any, Dict


def get_env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def aws_region() -> str:
    return get_env("AWS_REGION", get_env("AWS_DEFAULT_REGION", "us-east-1"))


def cognito_user_pool_id() -> str:
    return get_env("COGNITO_USER_POOL_ID")


def cognito_client_id() -> str:
    return get_env("COGNITO_APP_CLIENT_ID")


def openai_api_key() -> str:
    return get_env("OPENAI_API_KEY")


def pinecone_api_key() -> str:
    return get_env("PINECONE_API_KEY")


def firestore_project_id() -> str:
    return get_env("GOOGLE_CLOUD_PROJECT")


def request_headers(extra: Dict[str, str] | None = None) -> Dict[str, str]:
    headers = {"Content-Type": "application/x-amz-json-1.1"}
    if extra:
        headers.update(extra)
    return headers
