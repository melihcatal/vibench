import os

from openai import OpenAI

from storage_models import TranslationResult


def stored_text_translate(source_text: str, target_language: str = "en") -> TranslationResult:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Translate the following text to {target_language}: {source_text}",
    )
    translated = response.output_text
    return TranslationResult(source_text=source_text, translated_text=translated, target_language=target_language, raw={"model": "gpt-5.4-mini"})
