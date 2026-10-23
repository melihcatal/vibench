"""[LATER-STEP] localized_platform_output.py - Translate platform model output for another locale"""

import os
from translate import translator  # hypothetical utility
from model_client import get_managed_model_client
from model_models import PlatformInvocationResult


def translate_output(
    invocation_result: PlatformInvocationResult, target_lang: str = "es"
) -> str:
    """
    Translate the model's textual output to the requested locale using Google Cloud Translation.

    Args:
        invocation_result: Result from a model invocation.
        target_lang: BCP‑47 language tag (e.g., "es" for Spanish).
    Returns:
        The translated text.
    """
    # Ensure we have a client that provides the raw text (provider‑agnostic)
    if not hasattr(invocation_result, "data") or not isinstance(
        invocation_result.data, str
    ):
        raise ValueError("Only textual output is supported for translation")
    # Translate via the provider's SDK (here using google-cloud-translate as the concrete provider)
    translation_client = (
        translator.Translator()
    )  # imported from google-cloud-translate in real code
    translated = translation_client.translate(
        invocation_result.data, target_language=target_lang
    )
    return translated["translatedText"]  # concrete SDK return shape
