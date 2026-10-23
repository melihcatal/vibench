# translate_transcript.py
import os
import json
import boto3
import requests
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Example: python translate_transcript.py <transcript_text> <target_lang>
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: translate_transcript.py <transcript_text> <target_lang>", file=sys.stderr)
        sys.exit(1)
    transcript_text = sys.argv[1]
    target_lang = sys.argv[2].upper()

    # ---- IBM Watson Language Translator (example concrete provider) ----
    authenticator = IAMAuthenticator(os.getenv('IBM_WATSON_LANGUAGE_TRANSLATOR_APIKEY'))
    language_translator = LanguageTranslatorV3(
        version='2022-05-01',  # adjust as needed
        authenticator=authenticator
    )
    language_translator.set_service_url(os.getenv('IBM_WATSON_LANGUAGE_TRANSLATOR_URL'))

    response = language_translator.translate(
        text=[transcript_text],
        model_id=f'en-{target_lang.lower()}'  # e.g., 'en-es'
    ).get_result()

    translation = response.get('translations', [{}])[0].get('translation')
    print(json.dumps({"translation": translation}, indent=2))
