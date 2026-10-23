import os
from openai import OpenAI, AsyncOpenAI


def get_openai_api_key():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return api_key


def get_openai_organization():
    return os.environ.get("OPENAI_ORGANIZATION")


def get_openai_project():
    return os.environ.get("OPENAI_PROJECT")


def create_openai_client(**kwargs):
    api_key = get_openai_api_key()
    client_kwargs = {"api_key": api_key}
    org = get_openai_organization()
    if org:
        client_kwargs["organization"] = org
    project = get_openai_project()
    if project:
        client_kwargs["project"] = project
    client_kwargs.update(kwargs)
    return OpenAI(**client_kwargs)


def create_async_openai_client(**kwargs):
    api_key = get_openai_api_key()
    client_kwargs = {"api_key": api_key}
    org = get_openai_organization()
    if org:
        client_kwargs["organization"] = org
    project = get_openai_project()
    if project:
        client_kwargs["project"] = project
    client_kwargs.update(kwargs)
    return AsyncOpenAI(**client_kwargs)


OPENAI_API_BASE = "https://api.openai.com/v1"

SUPPORTED_OPENAI_MODELS = {
    "gpt-4o": {
        "family": "gpt-4",
        "capabilities": ["chat", "vision", "function_calling"],
    },
    "gpt-4o-mini": {
        "family": "gpt-4",
        "capabilities": ["chat", "vision", "function_calling"],
    },
    "gpt-4-turbo": {"family": "gpt-4", "capabilities": ["chat", "function_calling"]},
    "gpt-3.5-turbo": {"family": "gpt-3.5", "capabilities": ["chat"]},
    "o1": {"family": "o1", "capabilities": ["chat", "reasoning"]},
    "o1-mini": {"family": "o1", "capabilities": ["chat", "reasoning"]},
    "text-embedding-3-small": {"family": "embedding", "capabilities": ["embedding"]},
    "text-embedding-3-large": {"family": "embedding", "capabilities": ["embedding"]},
    "tts-1": {"family": "tts", "capabilities": ["audio"]},
    "tts-1-hd": {"family": "tts", "capabilities": ["audio"]},
    "whisper-1": {"family": "whisper", "capabilities": ["transcription"]},
}


def get_model_info(model_id):
    return SUPPORTED_OPENAI_MODELS.get(model_id)


def list_available_models():
    return list(SUPPORTED_OPENAI_MODELS.keys())
