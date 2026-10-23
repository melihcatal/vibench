import os
import requests
import uuid


def translate_text(text: str, to_language: str, from_language: str = "en") -> str:
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    endpoint = "https://api.cognitive.microsofttranslator.com"
    location = os.getenv("AZURE_TRANSLATOR_REGION")

    if not key or not location:
        raise ValueError(
            "AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION environment variables must be set."
        )

    path = "/translate"
    constructed_url = endpoint + path

    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Ocp-Apim-Subscription-Region": location,
        "Content-type": "application/json",
        "X-ClientTraceId": str(uuid.uuid4()),
    }

    params = {"api-version": "3.0", "from": from_language, "to": [to_language]}

    body = [{"text": text}]

    response = requests.post(constructed_url, params=params, headers=headers, json=body)
    response.raise_for_status()
    translation_result = response.json()
    return translation_result[0]["translations"][0]["text"]


if __name__ == "__main__":
    # Example usage
    text_to_translate = "Hello, how are you?"
    target_language = "es"
    print(f"Translating '{text_to_translate}' to {target_language}...")
    translated_text = translate_text(text_to_translate, target_language)
    print(f"Translated text: {translated_text}")

    text_to_translate_fr = "Bonjour, comment ça va ?"
    target_language_en = "en"
    print(
        f"\nTranslating '{text_to_translate_fr}' from French to {target_language_en}..."
    )
    translated_text_en = translate_text(
        text_to_translate_fr, target_language_en, from_language="fr"
    )
    print(f"Translated text: {translated_text_en}")
