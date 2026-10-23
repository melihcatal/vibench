import os

from openai import OpenAI


def quality_summary(translated_text: str, source_text: str) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Summarize quality issues between source and translation. Source: {source_text}\nTranslation: {translated_text}",
    )
    return response.output_text
