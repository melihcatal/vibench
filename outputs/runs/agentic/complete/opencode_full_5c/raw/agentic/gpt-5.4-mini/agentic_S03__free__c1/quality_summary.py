from openai import OpenAI

from translation_client import DEFAULT_MODEL, get_client


def quality_summary(text: str, source_language: str, target_language: str):
    client: OpenAI = get_client()
    prompt = f"Summarize translation quality issues for {source_language} to {target_language}: {text}"
    response = client.responses.create(model=DEFAULT_MODEL, input=prompt)
    return getattr(response, "output_text", "")
