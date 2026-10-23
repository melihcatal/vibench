import os

from openai import OpenAI


def main(text):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Check the following log text for unsafe content and return a brief verdict:\n{text}",
    )
    return response.output_text
