# translate_transcript.py

from speech_client import get_speech_client
from speech_models import TTranslationRequest, TTranslationResult
import requests, json


def translate_transcript(text: str, target_lang: str = "es") -> str:
    client = get_speech_client()
    # Use a separate translation service (e.g., Google Cloud Translation) for demo purposes
    trans_url = "https://translation.googleapis.com/language/translate/v2"
    payload = {"q": text, "target": target_lang, "key": os.getenv("TRANSLATE_API_KEY")}
    resp = requests.post(trans_url, json=payload)
    resp.raise_for_status()
    data = resp.json()
    return data["data"]["translations"][0]["translatedText"]


if __name__ == "__main__":
    import sys, json

    job_id = sys.argv[1]
    transcript_url = poll_transcription(
        job_id
    )  # reuse poll from earlier file if needed
    # In real usage, fetch the transcript first
    translated = translate_transcript("Hello world", "es")
    print(json.dumps({"translated_text": translated}))
