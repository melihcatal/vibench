import os
from typing import Optional, Any


def get_openai_client(api_key: Optional[str] = None) -> Any:
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    from openai import OpenAI

    return OpenAI(api_key=api_key)


def get_xai_client(api_key: Optional[str] = None) -> Any:
    api_key = api_key or os.getenv("XAI_API_KEY")
    from openai import OpenAI

    return OpenAI(base_url="https://api.x.ai/v1", api_key=api_key)


def get_anthropic_client(api_key: Optional[str] = None) -> Any:
    api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
    import anthropic

    return anthropic.Anthropic(api_key=api_key)


def get_google_model(
    model_name: str = "gemini-1.5-pro", api_key: Optional[str] = None
) -> Any:
    api_key = api_key or os.getenv("GOOGLE_API_KEY")
    import google.generativeai as genai

    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name=model_name)


def get_mistral_client(api_key: Optional[str] = None) -> Any:
    api_key = api_key or os.getenv("MISTRAL_API_KEY")
    from mistralai import Mistral

    return Mistral(api_key=api_key)
