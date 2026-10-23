import os
from translate_client import TranslateClient


# Later-step: Translate completed transcript segments
def translate_transcript(transcript, target_lang="es"):
    client = TranslateClient()
    # Provider SDK call (Google Cloud Translation example)
    translation = client.translator.translate(
        text=transcript, target_language=target_lang
    )
    return translation["translatedText"]


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: translate_transcript.py <transcript_text> [target_language]")
        sys.exit(1)
    transcript = sys.argv[1]
    target = sys.argv[2] if len(sys.argv) > 2 else "es"
    translated = translate_transcript(transcript, target)
    print(f"Translated transcript: {translated}")
