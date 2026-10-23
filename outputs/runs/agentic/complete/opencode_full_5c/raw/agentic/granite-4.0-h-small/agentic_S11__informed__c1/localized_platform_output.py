# [LATER-STEP] localized_platform_output.py
# Translate platform model output for another locale

from google.cloud import translate_v2 as translate
from model_models import ProviderResponse


def translate_output(output: str, target_locale: str = "es") -> str:
    """Translate raw model output to the requested locale using Google Translate."""
    gclient = translate.Client()
    result = gclient.translate(output, target_language=target_locale)
    return result["translatedText"]
