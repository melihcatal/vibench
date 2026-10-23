import os
import json
from ibm_watsonx_ai import WatsonxApi
from ibm_watsonx_ai.nlu import NluV1

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Initialize Watsonx NLU client for translation
translator = NluV1(base_url="https://api.watsonx.cloud", api_key=WATSONX_API_KEY)


def translate_compliance_note(note: str, target_lang: str = "es") -> str:
    """Translate encryption or compliance notes for reviewers using Watsonx.ai translation.

    Returns the translated text.
    """
    try:
        response = translator.translate(text=note, target=target_lang)
        translated = response.json().get("translation", "")
        return translated
    except Exception as e:
        raise RuntimeError(f"Translation failed: {e}")


# Simple CLI demo
if __name__ == "__main__":
    sample_note = (
        "All data at rest must be encrypted with AES-256 and meet GDPR requirements."
    )
    translated = translate_compliance_note(sample_note, target_lang="es")
    print(f"Original: {sample_note}\nSpanish: {translated}")
