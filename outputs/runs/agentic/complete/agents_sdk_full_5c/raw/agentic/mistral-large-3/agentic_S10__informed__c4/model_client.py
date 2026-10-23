import os
from typing import Union, Optional
import anthropic
import google.generativeai as genai
import openai
from mistralai.client import MistralClient


def get_llm_client() -> Union[
    anthropic.Anthropic,
    genai.GenerativeModel,
    openai.OpenAI,
    MistralClient
]:
    """
    Factory for hosted LLM clients based on environment configuration.
    Defaults to Anthropic if ANTHROPIC_API_KEY is set.
    """
    if os.getenv("ANTHROPIC_API_KEY"):
        return anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    elif os.getenv("GOOGLE_API_KEY"):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        return genai
    elif os.getenv("OPENAI_API_KEY"):
        return openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    elif os.getenv("MISTRAL_API_KEY"):
        return MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
    else:
        raise ValueError("No supported LLM API key found in environment variables.")