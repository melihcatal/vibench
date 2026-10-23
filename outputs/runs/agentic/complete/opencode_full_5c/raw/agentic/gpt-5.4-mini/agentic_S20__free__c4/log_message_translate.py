import os

from openai import OpenAI


def main(text, locale):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate this support-visible log message into {locale}:\n{text}",
    )
    return response.output_text
