import os

from openai import OpenAI


def unsafe_copy_check(text: str) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Check this localized copy for unsafe content and return a concise verdict: {text}",
    )
    return response.output_text
