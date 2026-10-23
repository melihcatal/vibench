import json
from model_client import ModelClient


def translate_result(
    output: str, target_lang: str = "en", model_name: str = "gpt-4o-mini"
) -> str:
    """Translate LLM output into a different language.

    Args:
        output (str): The original model response.
        target_lang (str): Target language code (ISO 639-1, default: "en").
        model_name (str): Hosted model identifier (default: gpt-4o-mini).

    Returns:
        str: Translated text.
    """
    client = ModelClient(model_name)
    prompt = f"Translate the following text into {target_lang} preserving tone and meaning:\n\n{output}"
    translated = client.complete(prompt)
    return translated["text"].strip()
