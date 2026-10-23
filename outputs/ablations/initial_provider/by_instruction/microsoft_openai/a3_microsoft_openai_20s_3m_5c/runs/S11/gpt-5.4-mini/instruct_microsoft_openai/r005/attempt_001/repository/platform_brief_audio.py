import os
from openai import AzureOpenAI
from model_client import build_azure_openai_client


def platform_brief_audio(text: str) -> bytes:
    client: AzureOpenAI = build_azure_openai_client()
    response = client.audio.speech.create(
        model=os.environ.get("AZURE_OPENAI_TTS_MODEL", "gpt-4o-mini-tts"),
        voice=os.environ.get("AZURE_OPENAI_TTS_VOICE", "alloy"),
        input=text,
    )
    return response.read()


if __name__ == "__main__":
    print(len(platform_brief_audio(os.environ.get("PLATFORM_TEXT", ""))))
