from openai import OpenAI

from translation_client import get_client, get_model_name
from translation_models import normalize_text


def quality_summary(
    source_text: str, translated_text: str, source_language: str, target_language: str
) -> str:
    client: OpenAI = get_client()
    prompt = (
        f"Review translation quality from {normalize_text(source_language)} to {normalize_text(target_language)}. "
        f"Source: {normalize_text(source_text)}. Translation: {normalize_text(translated_text)}. "
        "Summarize fluency, meaning preservation, and any issues."
    )
    result = client.responses.create(model=get_model_name(), input=prompt)
    return result.output_text
