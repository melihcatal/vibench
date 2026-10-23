# [LATER-STEP] translate_transcript.py
import os
import json
from typing import List, Dict
from speech_client import BatchSpeechClient
from speech_models import TranscriptionJobResult

# Provider used: DeepL Translator (https://api.deepl.com/v2/translate)
DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")


def translate_segments(
    segments: List[Dict[str, Any]], target_lang: str = "fr"
) -> List[Dict[str, Any]]:
    """
    Translate each transcription segment (e.g., Azure result) to the target language using DeepL.
    Returns a list of translated segment dicts.
    """
    translated: List[Dict[str, Any]] = []
    for seg in segments:
        text = seg["text"]
        # Simple DeepL API call (POST) – only the text field is translated.
        payload = {"auth_key": DEEPL_AUTH_KEY, "text": text, "target_lang": target_lang}
        resp = httpx.post("https://api.deepl.com/v2/translate", data=payload)
        resp.raise_for_status()
        translation = resp.json()["text"]
        seg_translated = {
            "original_text": text,
            "translated_text": translation,
            "start": seg["start"],
            "end": seg["end"],
            "speaker": seg.get("speaker"),
        }
        translated.append(seg_translated)
    return translated


if __name__ == "__main__":
    import sys
    import httpx
    from speech_client import BatchSpeechClient

    if len(sys.argv) != 3:
        print("Usage: translate_transcript.py <job_id> <target_lang>", file=sys.stderr)
        sys.exit(1)
    job_id = sys.argv[1]
    target_lang = sys.argv[2]
    client = BatchSpeechClient(
        os.getenv("AZURE_SPEECH_ENDPOINT"), os.getenv("AZURE_SPEECH_KEY")
    )
    result = json.loads(
        client.get_transcription_result(job_id, include_timestamps=False)
    )
    segments = result.get("segments", [])
    translations = translate_segments(segments, target_lang)
    print(json.dumps(translations, indent=2))
