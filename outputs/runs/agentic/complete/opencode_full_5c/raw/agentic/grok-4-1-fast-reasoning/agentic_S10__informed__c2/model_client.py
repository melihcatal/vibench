import os

DEFAULT_MODEL = "gpt-4o-mini"


def get_default_model() -> str:
    return os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
