import os
from openai import OpenAI


def appeal_translate(text: str, target_language: str = "en"):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = f"Translate this appeal text to {target_language}: {text}"
    response = client.responses.create(model="gpt-4.1-mini", input=prompt)
    return response.output_text
