import os

from openai import OpenAI


def main(text: str = "", locale: str = "es") -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.responses.create(model="gpt-5.4-mini", input=f"Translate this support log message to {locale}:\n{text}")
    return response.output_text
