import os
import json
import openai

# OpenAI API credentials (replace with real secrets in production)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


def translate_invoice_notes(extracted: dict, target_lang: str = "es") -> dict:
    """
    Translate extracted invoice notes/descriptions to another language using OpenAI's
    chat completions endpoint.
    Returns a dict with the translated text under the key 'translated_note'.
    """
    note = extracted.get("vendor_notes", "")
    if not note:
        return {"translated_note": ""}
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Translate the following to {target_lang}:",
                "translations": {"text": note},
            }
        ],
    )
    # Simplified extraction of translated content from response
    translated = response.choices[0].message.content.split('"text": "')[1].split('"')[0]
    return {"translated_note": translated}


# Example test (uncomment to run)
# invoice = {'vendor_notes':'The shipment will arrive next Monday.'}
# print(json.dumps(translate_invoice_notes(invoice), indent=2))
