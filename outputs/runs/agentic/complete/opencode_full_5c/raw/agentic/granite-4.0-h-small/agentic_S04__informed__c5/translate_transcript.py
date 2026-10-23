# [LATER-STEP] translate_transcript.py
# Translate completed transcript segments using Azure AI Translator SDK
import os
from azure.ai.translation.text import TranslationTextClient
from speech_client import get_auth_header

TRANSLATOR_ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
SOURCE_LOCALE = "en"
TARGET_LOCALE = "es"

client = TranslationTextClient(endpoint=TRANSLATOR_ENDPOINT, credential=TRANSLATOR_KEY)


def translate_segments(transcript: str) -> str:
    """
    Split transcript into sentences and translate each segment to the target locale.
    Returns the full translated text with sentence boundaries preserved.
    """
    # Simple naive sentence split (period followed by space)
    sentences = [s.strip() for s in transcript.split(". ") if s]
    translated_sentences = []
    for sentence in sentences:
        response = client.translate(
            text=sentence, source_language=SOURCE_LOCALE, target_language=TARGET_LOCALE
        )
        translated_sentences.append(response[0].translations[0].text)
    return ". ".join(translated_sentences)


if __name__ == "__main__":
    import sys, json

    if len(sys.argv) != 2:
        print("Usage: python translate_transcript.py <path-to-json-transcript>")
        sys.exit(1)
    with open(sys.argv[1], "r") as f:
        payload = json.load(f)
    raw_text = payload.get("text", payload.get("transcript", ""))
    translated = translate_segments(raw_text)
    print("Translated transcript:", translated)
