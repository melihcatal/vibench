import os
from dataclasses import dataclass

from openai import OpenAI


DEFAULT_OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
DEFAULT_AZURE_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", DEFAULT_OPENAI_MODEL)


@dataclass
class ModelConfig:
    provider: str
    model: str
    api_key: str | None = None
    base_url: str | None = None
    azure_endpoint: str | None = None
    api_version: str | None = None
    deployment: str | None = None


def load_config(provider: str = "openai", model: str | None = None) -> ModelConfig:
    provider = provider.lower()
    if provider == "azure":
        return ModelConfig(
            provider="azure",
            model=model or DEFAULT_AZURE_DEPLOYMENT,
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
            deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT", model or DEFAULT_AZURE_DEPLOYMENT),
        )
    return ModelConfig(
        provider="openai",
        model=model or DEFAULT_OPENAI_MODEL,
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_BASE_URL"),
    )


def build_client(config: ModelConfig) -> OpenAI:
    kwargs = {}
    if config.api_key:
        kwargs["api_key"] = config.api_key
    if config.base_url:
        kwargs["base_url"] = config.base_url
    if config.azure_endpoint:
        kwargs["base_url"] = config.azure_endpoint.rstrip("/") + "/openai"
    return OpenAI(**kwargs)


def select_model_family(task: str) -> str:
    task = task.lower()
    if any(key in task for key in ("embed", "embedding")):
        return os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-large")
    if any(key in task for key in ("translate", "spoken", "brief", "safety", "json", "summar", "answer", "stream")):
        return os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    return os.getenv("OPENAI_MODEL", "gpt-4o-mini")
