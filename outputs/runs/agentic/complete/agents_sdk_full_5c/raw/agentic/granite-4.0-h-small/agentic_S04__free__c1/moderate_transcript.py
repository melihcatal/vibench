import os
import json
from speech_client import BatchSpeechClient
from speech_models import TimestampedTranscript

# ------------------------------------------------------------
# moderate_transcript.py
# Moderate (sanitize) transcript text before publishing
# ------------------------------------------------------------

def moderate_transcript(job_id: str) -> str:
    """Fetch a transcript, sanitize profanity, and return cleaned text.

    For demonstration we perform a simple placeholder filter.
    """
    client = BatchSpeechClient()
    results = client.get_transcription_results(job_id)
    # The STT results endpoint returns a list of words with no timestamps
    words = results.get("results", [])
    sanitized = [w.replace("badword", "[censored]").lower() for w in words]
    cleaned_text = " ".join(sanitized)
    return cleaned_text

# Example usage (run as script)
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Moderate a transcription result.")
    parser.add_argument("job_id", help="Transcription job ID.")
    args = parser.parse_args()
    clean = moderate_transcript(args.job_id)
    print(clean)
