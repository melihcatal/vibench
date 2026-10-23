import os
from functools import lru_cache


def _env(*names, default=None):
    for name in names:
        value = os.getenv(name)
        if value:
            return value
    return default


@lru_cache(maxsize=1)
def tts_client():
    from openai import OpenAI

    return OpenAI(api_key=_env("OPENAI_API_KEY", "AZURE_OPENAI_API_KEY"))


def tts_model():
    return _env("OPENAI_TTS_MODEL", default="gpt-4o-mini-tts")


def translator_client():
    from openai import OpenAI

    return OpenAI(api_key=_env("OPENAI_API_KEY"))


def translator_model():
    return _env("OPENAI_TRANSLATION_MODEL", default="gpt-4o-mini")


def safety_client():
    from openai import OpenAI

    return OpenAI(api_key=_env("OPENAI_API_KEY"))


def embedding_client():
    from openai import OpenAI

    return OpenAI(api_key=_env("OPENAI_API_KEY"))


def transcription_client():
    from openai import OpenAI

    return OpenAI(api_key=_env("OPENAI_API_KEY"))
