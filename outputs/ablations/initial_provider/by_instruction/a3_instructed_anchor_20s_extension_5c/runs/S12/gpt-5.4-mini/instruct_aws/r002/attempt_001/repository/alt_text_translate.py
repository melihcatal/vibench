import os

from openai import OpenAI


def alt_text_translate(text, target_language):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate this image description to {target_language}: {text}",
    )
    return response.output_text
