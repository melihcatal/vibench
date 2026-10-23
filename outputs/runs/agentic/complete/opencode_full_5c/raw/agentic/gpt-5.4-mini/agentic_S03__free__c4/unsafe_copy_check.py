import os

from openai import OpenAI


def unsafe_copy_check(copy_text: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Check for unsafe localized copy. Text: {copy_text}",
    )
    return response.output_text
