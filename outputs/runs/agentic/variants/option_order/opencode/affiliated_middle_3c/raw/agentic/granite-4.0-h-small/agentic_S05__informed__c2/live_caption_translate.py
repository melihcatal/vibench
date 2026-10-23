import json
import requests
from speech_models import normalize_transcript, SpeechRecognitionResult

# Google Cloud Translation (example service)
API_KEY = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS"
)  # expects env var with path to credentials
TRANSLATE_URL = "https://translation.googleapis.com/language/translate/v2"


def translate_captions(source_text: str, target_lang: str = "es") -> str:
    """Translates live captions using Google Cloud Translation API.
    Args:
        source_text (str): text to translate
        target_lang (str): target language code (default 'es')
    Returns:
        str: translated text
    """
    payload = {"q": source_text, "target": target_lang, "format": "text"}
    response = requests.post(TRANSLATE_URL, params={"key": API_KEY}, data=payload)
    data = response.json()
    translated = data["data"]["translations"][0]["translatedText"]
    return translated


# Example processing flow (placeholder)
# async for chunk in stream_microphone():
#     event = parse_event(json.loads(chunk))  # from partial_results
#     if event.is_final:
#         translation = translate_captions(event.transcript)
#         print('TRANSLATED:', translation)
