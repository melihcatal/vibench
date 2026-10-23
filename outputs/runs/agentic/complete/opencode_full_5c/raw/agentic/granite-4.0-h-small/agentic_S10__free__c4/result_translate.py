import json
import os
from model_client import HostedModelClient


def translate_output(text: str, target_lang: str = "es") -> str:
    """Translates generated model output to a target language using a hosted model.

    Args:
        text: Original model output.
        target_lang: Two-letter language code for the target language.

    Returns:
        The translated text.
    """
    client = HostedModelClient(model="gpt-4o")
    prompt = (
        f"Translate the following English text to {target_lang} language:\n\n{text}"
    )
    payload = {"prompt": prompt, "temperature": 0.0}
    response = client.chat_completion(payload)
    translated = response["choices"][0]["message"]["content"]
    return translated.strip()
