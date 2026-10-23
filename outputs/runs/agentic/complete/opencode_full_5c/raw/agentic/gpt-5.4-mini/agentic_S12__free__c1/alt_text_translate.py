from openai import OpenAI
from vision_client import OPENAI_API_HOST, OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_API_HOST)


def alt_text_translate(text: str, target_language: str) -> str:
    prompt = f"Translate this image description to {target_language}: {text}"
    resp = client.responses.create(model="gpt-4o-mini", input=prompt)
    return resp.output_text
