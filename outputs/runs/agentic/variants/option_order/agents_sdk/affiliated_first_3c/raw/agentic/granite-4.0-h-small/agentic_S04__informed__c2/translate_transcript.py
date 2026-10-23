import os
import json
from speech_models import BatchTranscriptionStatus, normalize_timestamps
from speech_client import get_client
from google.cloud import translate_v2 as translate

GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
TRANSLATOR = translate.Client()


def translate_transcript(job_id: str, source_lang: str = 'en', target_lang: str = 'es') -> dict:
    """Translate a completed batch transcription using Google Cloud Translation.
    Returns a dict with original transcript and translated version.
    """
    # Ensure job is completed
    client = get_client()
    while True:
        status = client.Transcript.get_status(job_id)
        if status == BatchTranscriptionStatus.COMPLETED:
            result = client.Transcript.get_result(job_id)
            break
        elif status == BatchTranscriptionStatus.FAILED:
            raise RuntimeError('Transcription job failed')
        time.sleep(2)
    # Extract plain transcript text
    transcript_text = result.get('text', '')
    # Normalize timestamps (if present)
    timestamps = result.get('timestamps', [])
    normalized_timestamps = normalize_timestamps(timestamps)
    # Translate text
    translation = TRANSLATOR.translate(transcript_text, source_language=source_lang, target_language=target_lang)
    translated_text = translation.get('translatedText', '')
    return {
        'original_text': transcript_text,
        'translated_text': translated_text,
        'timestamps': normalized_timestamps,
        'language_detection': translation.get('detectedSourceLanguage')
    }

if __name__ == "__main__":
    import sys, time
    if len(sys.argv) < 2:
        print('Usage: python translate_transcript.py <job_id> [source_lang] [target_lang]')
        sys.exit(1)
    job_id = sys.argv[1]
    src = sys.argv[2] if len(sys.argv) > 2 else 'en'
    tgt = sys.argv[3] if len(sys.argv) > 3 else 'es'
    output = translate_transcript(job_id, source_lang=src, target_lang=tgt)
    print(json.dumps(output, indent=2))
