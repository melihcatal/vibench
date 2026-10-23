import os

from openai import AzureOpenAI


def platform_brief_audio(text: str) -> dict:
    client = AzureOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
        api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01"),
    )
    response = client.audio.speech.create(
        model=os.getenv("AZURE_OPENAI_TTS_MODEL", "gpt-4o-mini-tts"),
        voice=os.getenv("AZURE_OPENAI_TTS_VOICE", "alloy"),
        input=text,
    )
    return {
        "provider": "azure-openai",
        "raw": response,
        "model": os.getenv("AZURE_OPENAI_TTS_MODEL", "gpt-4o-mini-tts"),
    }
