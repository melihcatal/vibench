import os
from typing import Optional, Any


def get_openai_client() -> Optional[Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    from openai import OpenAI

    return OpenAI(api_key=api_key)


def get_anthropic_client() -> Optional[Any]:
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return None
    from anthropic import Anthropic

    return Anthropic(api_key=api_key)


def get_perspective_service() -> Optional[Any]:
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    if not api_key:
        return None
    from googleapiclient.discovery import build

    return build("commentanalyzer", "v1alpha1", developerKey=api_key)


def get_elevenlabs_client() -> Optional[Any]:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        return None
    from elevenlabs.client import ElevenLabs

    return ElevenLabs(api_key=api_key)
