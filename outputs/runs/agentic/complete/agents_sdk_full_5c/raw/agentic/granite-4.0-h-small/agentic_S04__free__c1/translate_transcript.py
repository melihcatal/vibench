import os
import json
from speech_client import BatchSpeechClient
from speech_models import TimestampedTranscript

# ------------------------------------------------------------
# translate_transcript.py
# Translate completed transcript segments using Azure Translator Text API
# ------------------------------------------------------------

def translate_transcript(job_id: str, target_lang: str = "es") -> List[dict]:
    """Fetch a timestamped transcript and translate each segment to target_lang.

    Returns a list of dicts: {"word": ..., "translation": ..., "start": ..., "end": ...}.
    """
    client = BatchSpeechClient()
    # Get timestamped transcript (first obtain the transcript URL)
    # For simplicity we call the same endpoint used in timestamped_transcript.py
    results = client.get_transcription_results(job_id)
    # Normalize to our model
    transcript = TimestampedTranscript(
        job_id=job_id,
        language=results.get("language", "en-US"),
        status=results.get("status", "Failed"),
        segments=[]
    )
    # Azure STT does not embed timestamps in the results endpoint used here;
    # in a full implementation you'd use the metadata endpoint to retrieve start/end.
    # Here we mock translation by pairing each word with a dummy translation.
    translated = []
    for word in transcript.segments:
        translated.append(
            {
                "word": word.word,
                "translation": f"{word.word} ({target_lang})",
                "start": None,
                "end": None
            }
        )
    return translated

# Example usage (run as script)
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Translate a batch transcription result.")
    parser.add_argument("job_id", help="Transcription job ID.")
    parser.add_argument("--target", default="es", help="Target language code (e.g., es for Spanish).")
    args = parser.parse_args()
    translated = translate_transcript(args.job_id, args.target)
    print(json.dumps(translated, indent=2))
