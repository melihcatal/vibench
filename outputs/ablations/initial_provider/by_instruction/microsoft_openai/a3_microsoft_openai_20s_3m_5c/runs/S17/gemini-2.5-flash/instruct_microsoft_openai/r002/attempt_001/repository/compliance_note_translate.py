import os
import argparse
from security_client import SecurityClient
from security_models import TranslationRequest, TranslationResponse

def compliance_note_translate_main():
    parser = argparse.ArgumentParser(description="Translate encryption or compliance notes for reviewers using Azure AI Translator.")
    parser.add_argument("--text", required=True, help="The note text to translate.")
    parser.add_argument("--from-lang", default="en", help="Source language code (e.g., 'en', 'fr').")
    parser.add_argument("--to-lang", default="es", help="Target language code (e.g., 'es', 'de').")
    parser.add_argument("--translator-endpoint", required=False, 
                        help="The Azure Translator endpoint. Defaults to AZURE_TRANSLATOR_ENDPOINT environment variable.")
    parser.add_argument("--translator-api-key", required=False, 
                        help="The Azure Translator API key. Defaults to AZURE_TRANSLATOR_API_KEY environment variable.")

    args = parser.parse_args()

    translator_endpoint = args.translator_endpoint or os.environ.get("AZURE_TRANSLATOR_ENDPOINT")
    translator_api_key = args.translator_api_key or os.environ.get("AZURE_TRANSLATOR_API_KEY")

    if not translator_endpoint or not translator_api_key:
        raise ValueError("Azure Translator endpoint and API key not provided. Please set relevant arguments or environment variables.")

    client = SecurityClient()
    request = TranslationRequest(
        text=args.text,
        from_lang=args.from_lang,
        to_lang=args.to_lang
    )

    try:
        response: TranslationResponse = client.translate_text(request)
        print(f"Original text ({args.from_lang}): {args.text}")
        print(f"Translated text ({args.to_lang}): {response.translated_text}")
    except Exception as e:
        print(f"Translation failed: {e}")

if __name__ == "__main__":
    compliance_note_translate_main()
