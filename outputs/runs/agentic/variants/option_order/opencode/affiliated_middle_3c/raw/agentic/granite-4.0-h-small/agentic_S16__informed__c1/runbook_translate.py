# runbook_translate.py
# Translates secret rotation runbook notes from one language to another using a hosted LLM.
import os
import json
from security_models import normalize_secret_payload
from dashscope import Client

# Choose the hosted LLM service
# For this example we use the Gemini API (Google Gemini) via the SDK
client = Client(api_key=os.getenv("GOOGLE_API_KEY"))


def translate_runbook(note: str, target_lang: str = "es") -> str:
    """Translate a secret rotation runbook note using hosted LLM inference.

    Args:
        note (str): The original runbook instruction text.
        target_lang (str): ISO language code for the desired output language.

    Returns:
        str: Translated text.
    """
    response = client.chat.completions.create(
        model="gemini-1.5-pro",
        messages=[
            {
                "role": "user",
                "content": f"Translate the following note to {target_lang}:\n\n{note}",
            }
        ],
        temperature=0.0,
        max_output_tokens=500,
    )
    translated = response["choices"][0]["message"]["content"]
    return translated.strip()


if __name__ == "__main__":
    sample_note = "Rotate secret version 2. Ensure all dependent services receive the new credentials within 5 minutes."
    translated = translate_runbook(sample_note, target_lang="es")
    print("Original:", sample_note)
    print("Spanish translation:", translated)
