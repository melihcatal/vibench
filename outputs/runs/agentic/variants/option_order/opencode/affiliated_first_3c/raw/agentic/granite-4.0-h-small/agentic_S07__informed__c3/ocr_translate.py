import os
import requests

# ---------- Provider credentials ----------
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
GOOGLE_CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
AZURE_TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
AZURE_TRANSLATOR_REGION = os.getenv("AZURE_TRANSLATOR_REGION")

# ---------- Translation using DeepL SDK ----------
try:
    from deepl import DeepL
except ImportError:
    DeepL = None


def translate_text(text: str, target_lang: str = "EN") -> str:
    """
    Translate raw OCR text to English (default) using the selected provider.

    Priority order:
      1. DeepL SDK (preferred)
      2. Google Cloud Translation
      3. Azure AI Translator (REST)
    """

    if DeepL is not None and DEEPL_AUTH_KEY:
        # Use DeepL Python client
        client = DeepL(auth_key=DEEPL_AUTH_KEY)
        translation = client.translate_text(text, target_lang=target_lang)
        return translation.text

    # Fallback to Google Cloud Translation
    if GOOGLE_CREDENTIALS_PATH:
        try:
            from google.cloud import translate_v2 as translate

            translate_client = translate.Client.from_service_account_json(
                GOOGLE_CREDENTIALS_PATH
            )
            result = translate_client.translate(text, target_language=target_lang)
            return result["translatedText"]
        except Exception as e:
            print("Google translation failed:", e)

    # Fallback to Azure Translator REST API
    if AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION:
        try:
            endpoint = f"https://{AZURE_TRANSLATOR_REGION}.api.cognitive.microsofttranslator.com"
            path = "/translate?api-version=3.0&to={lang}".format(lang=target_lang)
            url = endpoint + path
            headers = {
                "Ocp-Apim-Subscription-Key": AZURE_TRANSLATOR_KEY,
                "Content-Type": "application/json",
            }
            body = [{"Text": text}]
            resp = requests.post(url, headers=headers, json=body)
            resp.raise_for_status()
            return resp.json()[0]["translations"][0]["text"]
        except Exception as e:
            print("Azure translation failed:", e)

    raise RuntimeError("No translation provider configured")


# Example usage (run as script)
if __name__ == "__main__":
    raw_ocr = "Bonjour tout le monde"
    translated = translate_text(raw_ocr, target_lang="EN")
    print("Translated text:", translated)
