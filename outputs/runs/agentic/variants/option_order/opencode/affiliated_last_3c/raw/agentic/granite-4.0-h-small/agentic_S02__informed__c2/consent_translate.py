from typing import List, Dict
import os
from google.cloud import translate_v2 as translate


def translate_consent_copies(copies: List[Dict], target_lang: str = "es") -> List[Dict]:
    """Translate provider consent text documents to a target language.
    Uses Google Cloud Translation SDK. Set GOOGLE_APPLICATION_CREDENTIALS env var.
    """
    client = translate.Client()
    translated = []
    for copy in copies:
        doc_id = copy.get("doc_id")
        source_text = copy.get("text")
        if not source_text:
            raise ValueError("Missing text for doc_id " + str(doc_id))
        # Google expects a string or a list of strings
        response = client.translate(source_text, target_language=target_lang)
        translated.append({**copy, "translated_text": response["translatedText"]})
    return translated


# Local testing stub (requires GOOGLE_APPLICATION_CREDENTIALS set)
if __name__ == "__main__":
    sample_copies = [
        {"doc_id": "001", "text": "I agree to share my email address."},
        {"doc_id": "002", "text": "Please share my profile picture."},
    ]
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
        "/path/to/google-creds.json"  # ensure set
    )
    print(translate_consent_copies(sample_copies))
