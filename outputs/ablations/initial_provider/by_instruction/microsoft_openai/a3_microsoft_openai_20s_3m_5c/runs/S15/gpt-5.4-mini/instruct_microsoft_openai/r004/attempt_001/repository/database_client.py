import os
from functools import lru_cache

from openai import OpenAI


def get_database_endpoint() -> str:
    return os.getenv("COSMOS_DB_ENDPOINT", "")


def get_database_key() -> str:
    return os.getenv("COSMOS_DB_KEY", "")


def get_database_name() -> str:
    return os.getenv("COSMOS_DB_NAME", "documents")


def get_container_name() -> str:
    return os.getenv("COSMOS_DB_CONTAINER", "records")


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def provider_name() -> str:
    return "microsoft-azure-cosmos-db"
