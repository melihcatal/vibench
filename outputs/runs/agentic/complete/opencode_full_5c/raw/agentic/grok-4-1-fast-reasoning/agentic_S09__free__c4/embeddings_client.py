import os
import openai
import cohere
from voyageai import Voyage
import anthropic
import deepl


def get_openai_client(base_url: str = None) -> openai.OpenAI:
    kwargs = {"api_key": os.getenv("OPENAI_API_KEY")}
    if base_url:
        kwargs["base_url"] = base_url
    return openai.OpenAI(**kwargs)


def get_cohere_client() -> cohere.Cohere:
    return cohere.Cohere(api_key=os.getenv("COHERE_API_KEY"))


def get_voyage_client() -> Voyage:
    return Voyage(api_key=os.getenv("VOYAGE_API_KEY"))


def get_anthropic_client() -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def get_deepl_translator() -> deepl.Translator:
    return deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
