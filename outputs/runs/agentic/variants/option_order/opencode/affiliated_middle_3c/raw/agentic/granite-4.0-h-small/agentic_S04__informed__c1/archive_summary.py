import json
from speech_models import TranscriptionResult, normalize_transcript
from summarization_client import Summarizer


def archive_summary(transcript: TranscriptionResult, max_words: int = 100) -> str:
    """Generate a concise summary suitable for archiving.

    Args:
        transcript (TranscriptionResult): Normalized transcript segments.
        max_words (int): Target word count for the summary.

    Returns:
        str: Human‑readable summary.
    """
    summarizer = Summarizer()
    # Concatenate all non‑blank segment texts
    full_text = " ".join(
        seg["text"] for seg in transcript["segments"] if seg["text"].strip()
    )
    # Ask the LLM to summarize while respecting word limit
    prompt = f"Summarize the following transcript in at most {max_words} words:\n\n{full_text}"
    response = summarizer.summarize(prompt)
    return response["summary"]


# Example (uncomment to test)
# if __name__ == "__main__":
#     job = {"job_id": "job_123", "language": "en"}
#     result = poll_transcription(job["job_id"])
#     norm = normalize_transcript(result)
#     summary = archive_summary(norm)
#     print(summary)
