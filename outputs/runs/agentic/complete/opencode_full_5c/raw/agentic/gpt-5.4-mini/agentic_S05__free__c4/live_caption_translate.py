from openai import OpenAI
from speech_client import load_config

async def live_caption_translate(text: str, target_language: str) -> str:
    client = OpenAI(api_key=load_config().openai_api_key)
    resp = client.responses.create(
        model="gpt-4o-mini",
        input=f"Translate this caption into {target_language}: {text}",
    )
    return resp.output_text
