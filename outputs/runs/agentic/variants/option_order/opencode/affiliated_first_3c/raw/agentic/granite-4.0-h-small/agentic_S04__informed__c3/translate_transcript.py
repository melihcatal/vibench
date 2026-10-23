# LATER-STEP translate completed transcript segments using DeepL API
import os
import requests
import json


def translate_transcript(transcript_text, target_lang="es"):
    """Translate transcript text with DeepL API.

    Args:
        transcript_text (str): The plain text of the transcript to translate.
        target_lang (str): ISO language code for the target language.

    Returns:
        str: Translated transcript.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY environment variable not set")
    payload = {
        "text": transcript_text,
        "target_lang": target_lang,
    }
    headers = {"Content-Type": "application/json"}
    resp = requests.post(
        "https://api.deepl.com/v2/translate",
        data=json.dumps(payload),
        headers=headers,
        auth=(auth_key,),  # DeepL uses basic auth where username is the key
    )
    resp.raise_for_status()
    result = resp.json()
    return result["translations"][0]["text"]


# Example CLI wrapper
if __name__ == "__main__":
    import sys

    transcript = sys.stdin.read()
    if not transcript:
        raise RuntimeError("No transcript provided via stdin")
    translated = translate_transcript(transcript)
    print(translated)
