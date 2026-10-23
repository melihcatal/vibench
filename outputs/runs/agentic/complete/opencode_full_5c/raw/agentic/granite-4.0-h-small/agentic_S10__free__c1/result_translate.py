import json
from model_client import create_client
from model_models import normalize


def translate_result(
    text: str, target_lang: str = "es", model: str = "gpt-4o-mini"
) -> str:
    """Translate model output to another language.

    Args:
        text (str): The source text to translate.
        target_lang (str): Target language code (e.g., 'es' for Spanish).
        model (str): Model family for translation.

    Returns:
        str: Translated text.
    """
    client = create_client(model)
    prompt = f"Translate the following text into {target_lang.upper()}:\n\n{text}"
    raw = client.chat_completion(messages=[{"role": "user", "content": prompt}])
    return normalize(raw).choices[0].message.content.strip()
