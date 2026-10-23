from openai import AzureOpenAI

from model_client import build_azure_openai_client


def platform_brief_audio(text: str):
    client = build_azure_openai_client()
    response = client.audio.speech.create(model="gpt-4o-mini-tts", voice="alloy", input=text)
    return response
