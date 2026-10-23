import os
import json
from speech_client import BatchSpeechClient
from speech_models import TimestampedTranscript

# ------------------------------------------------------------
# archive_summary.py
# Summarize a completed transcription for archiving
# ------------------------------------------------------------

def summarize_transcript(job_id: str) -> dict:
    """Fetch a transcript, summarize content, and produce an archive record.

    Returns a dict containing job_id, summary, word_count, and language.
    """
    client = BatchSpeechClient()
    results = client.get_transcription_results(job_id)
    # In real STT the results include timestamps; here we only have words.
    words = results.get("results", [])
    count = len(words)
    # Simple word frequency summary
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    summary = {
        "job_id": job_id,
        "language": results.get("language", "en-US"),
        "word_count": count,
        "summary": f"{count} words. Top terms: {', '.join(list(freq.keys())[:5])}"
    }
    return summary

# Example usage (run as script)
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Create an archive summary for a batch transcription.")
    parser.add_argument("job_id", help="Transcription job ID.")
    args = parser.parse_args()
    summary = summarize_transcript(args.job_id)
    print(json.dumps(summary, indent=2))
