import os
from functools import lru_cache

from openai import OpenAI


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def get_secret_model() -> str:
    return os.environ.get("OPENAI_SECRET_MODEL", "gpt-5.4-mini")


def get_secret_name(default: str) -> str:
    return os.environ.get("SECRET_NAME", default)


def get_secret_version() -> str:
    return os.environ.get("SECRET_VERSION", "latest")


def get_secret_stage() -> str:
    return os.environ.get("SECRET_STAGE", "current")
