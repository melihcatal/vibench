import os
from typing import Optional
from openai import OpenAI
from pydantic import BaseSettings


class EmbeddingsConfig(BaseSettings):
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_organization: Optional[str] = os.getenv("OPENAI_ORGANIZATION_ID", None)
    openai_project: Optional[str] = os.getenv("OPENAI_PROJECT_ID", None)


def get_embeddings_client() -> OpenAI:
    """Initialize and return an OpenAI client configured for embeddings."""
    config = EmbeddingsConfig()

    if not config.openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")

    client = OpenAI(
        api_key=config.openai_api_key,
        organization=config.openai_organization,
        project=config.openai_project,
    )
    return client
