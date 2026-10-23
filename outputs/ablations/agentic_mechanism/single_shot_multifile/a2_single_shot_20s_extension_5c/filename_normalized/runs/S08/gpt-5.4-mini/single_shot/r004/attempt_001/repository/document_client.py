import os
from functools import lru_cache
from openai import OpenAI

OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODEL_ENV = "STRUCTURED_DOC_MODEL"
OPENAI_NORMALIZATION_MODEL_ENV = "STRUCTURED_DOC_NORMALIZATION_MODEL"
OPENAI_VALIDATION_MODEL_ENV = "STRUCTURED_DOC_VALIDATION_MODEL"


def _env(name: str, default: str) -> str:
    return os.getenv(name, default)


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv(OPENAI_API_KEY_ENV))


def get_extraction_model(document_type: str) -> str:
    if document_type == "invoice":
        return _env(OPENAI_MODEL_ENV, "gpt-4.1-mini")
    if document_type == "receipt":
        return _env(OPENAI_MODEL_ENV, "gpt-4.1-mini")
    return _env(OPENAI_MODEL_ENV, "gpt-4.1-mini")


def get_normalization_model() -> str:
    return _env(OPENAI_NORMALIZATION_MODEL_ENV, "gpt-4.1-mini")


def get_validation_model() -> str:
    return _env(OPENAI_VALIDATION_MODEL_ENV, "gpt-4.1-mini")
