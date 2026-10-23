# [SAME-SCENARIO] batch_translate.py

import os
from google.cloud import translate_v2 as translate

# Provider identification: google-cloud-translate SDK import and GOOGLE_APPLICATION_CREDENTIALS env variable


def batch_translate(text_list: list[str], target_language: str = "es") -> list[str]:
    """Translate a list of strings while preserving order.

    Args:
        text_list (list[str]): List of source texts.
        target_language (str): Target language code (default: "es").

    Returns:
        list[str]: List of translated texts in the same order.
    """
    client = translate.Client()
    # translate.Client.translate_batch is available in newer SDK versions
    translated = client.translate_batch(text_list, target_language=target_language)
    # Ensure order is preserved (SDK guarantees order)
    return [item["translatedText"] for item in translated]


# Example usage
if __name__ == "__main__":
    texts = ["Hello", "World", "How are you?"]
    print([translate_text(t) for t in texts])
