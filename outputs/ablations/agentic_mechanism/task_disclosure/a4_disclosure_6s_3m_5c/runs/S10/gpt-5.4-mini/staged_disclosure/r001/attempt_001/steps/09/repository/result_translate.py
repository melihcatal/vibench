import os
from openai import OpenAI


def translate_result(text: str, target_language: str = "en") -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    prompt = f"Translate the following model output into {target_language}. Preserve meaning, formatting, and any code or structured data exactly when possible. Return only the translated text.\n\n{text}"
    response = client.responses.create(model="gpt-5.4-mini", input=prompt)
    return response.output_text
