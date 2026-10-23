from openai import OpenAI
from speech_client import load_config

async def live_caption_safety(text: str) -> bool:
    client = OpenAI(api_key=load_config().openai_api_key)
    resp = client.responses.create(
        model="gpt-4o-mini",
        input=f"Classify whether the following transcript is unsafe. Return only yes or no: {text}",
    )
    return resp.output_text.strip().lower().startswith("no")
