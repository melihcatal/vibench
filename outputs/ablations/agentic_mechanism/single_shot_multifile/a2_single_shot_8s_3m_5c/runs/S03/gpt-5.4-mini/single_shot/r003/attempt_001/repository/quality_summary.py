import os
from openai import OpenAI

_PROVIDER_MODEL = os.getenv("OPENAI_QUALITY_MODEL", "gpt-4o-mini")


def quality_summary(translation: str, source_text: str, source_language: str, target_language: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if os.getenv("OPENAI_API_KEY") else OpenAI()
    prompt = f'Summarize translation quality issues for a translation from {source_language} to {target_language}. Source: {source_text} Translation: {translation} Return a concise quality summary.'
    response = client.responses.create(model=_PROVIDER_MODEL, input=prompt)
    output_text = getattr(response, "output_text", None)
    if not output_text:
        output_text = response.output[0].content[0].text
    return output_text.strip()
