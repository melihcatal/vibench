from openai import OpenAI

from speech_client import create_openai_client, load_speech_config


def translate_live_caption(text: str, target_language: str) -> str:
    config = load_speech_config()
    client: OpenAI = create_openai_client(config)
    response = client.responses.create(model="gpt-4o-mini", input=f"Translate to {target_language}: {text}")
    return getattr(response, "output_text", "")
