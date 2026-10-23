import os
from model_client import ManagedModelClient
from model_models import InvocationRequest, InvocationResponse
import googletrans

def localized_platform_output(text: str, target_locale: str = "es") -> str:
    """
    Translate platform model output to another locale using a provider translation API or OSS library.
    This example uses googletrans (OSS) as a stand‑in for a provider translation service.
    """
    client = ManagedModelClient()
    # Translate using googletrans library (provider‑agnostic example)
    translator = googletrans.Translator()
    translated = translator.translate(text, dest=target_locale).text
    return translated

if __name__ == "__main__":
    original = "The weather is sunny."
    spanish = localized_platform_output(original, target_locale="es")
    print("Original:", original)
    print("Spanish translation:", spanish)