import os

from openai import OpenAI


def quality_summary(translated_text: str) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Summarize translation quality issues in this text: {translated_text}",
    )
    return response.output_text
