import os
from google.cloud import translate_v2 as translate
from observability_client import get_log_client, put_log

# Google Cloud Translation API
# Requires environment variable GOOGLE_APPLICATION_CREDENTIALS and TARGET_LOCALE (e.g., 'es', 'fr')

TARGET_LOCALE = os.getenv('TARGET_LOCALE', 'es')
if not TARGET_LOCALE:
    raise RuntimeError('Set TARGET_LOCALE environment variable')

translate_client = translate.Client()


def translate_log_message(message: str) -> str:
    """Translate log message text to the configured target locale.

    :param message: Raw log message.
    :return: Translated message.
    """
    result = translate_client.translate(message, target_language=TARGET_LOCALE)
    return result['translatedText']
