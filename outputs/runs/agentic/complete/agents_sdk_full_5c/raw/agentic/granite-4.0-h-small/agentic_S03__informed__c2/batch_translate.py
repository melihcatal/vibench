import os
from translation_client import TranslationClient
from typing import List

def batch_translate(texts: List[str], target_lang: str = "es") -> List[str]:
    """Translate a list of strings while preserving order.

    Args:
        texts: List of source strings.
        target_lang: Target language code (ISO 639-1).
    Returns:
        List of translated strings in the same order as input.
    """
    client = TranslationClient()
    if target_lang not in client.supported_languages:
        raise ValueError(f"Target language {target_lang} not supported.")
    # Most providers support batch translation via the same translate call when passing a list.
    # Fallback: translate each string individually if the client does not support true batch.
    if hasattr(client, "translate_batch"):
        responses = client.translate_batch(texts, target_lang)
    else:
        responses = [client.translate(t, target_lang) for t in texts]
    # Ensure each response contains the translated text.
    return [resp.get("translatedText", t) for t, resp in zip(texts, responses)]

# Example usage (remove in production)
if __name__ == "__main__":
    sample = ["Hello", "World", "How are you?"]
    print(batch_translate(sample, "fr"))
