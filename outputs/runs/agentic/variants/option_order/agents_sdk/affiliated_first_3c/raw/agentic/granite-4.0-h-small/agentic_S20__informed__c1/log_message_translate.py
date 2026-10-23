from google.cloud import translate_v2 as translate
from google.cloud.translate import enums
from observability_models import LogEntry
from typing import List, Dict

def translate_log_message(text: str, target_locale: str = "es") -> str:
    """Translate support-visible log messages for another locale.

    Args:
        text: Original message text.
        target_locale: Locale code (e.g., 'es', 'fr').
    Returns:
        Translated text string.
    """
    client = translate.Client()
    result = client.translate(text, target_language=target_locale)
    # result['translatedText'] holds the translation
    return result['translatedText']


def batch_translate_log_messages(messages: List[str], target_locale: str = "es") -> List[Dict[str, str]]:
    """Translate a batch of log messages, returning mapping of original to translated.

    Args:
        messages: List of log message strings.
        target_locale: Locale code.
    Returns:
        List of dictionaries with 'original' and 'translated' keys.
    """
    client = translate.Client()
    # Batch translation via the client's batch method
    responses = client.translate_batch(messages, target_language=target_locale)
    result = []
    for original, translated in zip(messages, responses):
        result.append({
            "original": original,
            "translated": translated['translatedText']
        })
    return result
