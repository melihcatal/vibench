# [SAME-SCENARIO] timestamped_transcript.py
import os
from typing import List, Dict
from speech_client import BatchSpeechClient

# Provider used: Azure Cognitive Services Speech-to-Text (Batch API with timestamps)
client = BatchSpeechClient(
    os.getenv("AZURE_SPEECH_ENDPOINT"), os.getenv("AZURE_SPEECH_KEY")
)


def fetch_timestamped_transcript(job_id: str) -> List[Dict[str, str]]:
    """Retrieve a transcription result with word-level timestamps.

    Args:
        job_id: ID of the completed transcription job.

    Returns:
        List[Dict]: Each dict contains 'start', 'end', 'text', and 'speaker' fields.
    """
    result = client.get_transcription_result(job_id, include_timestamps=True)
    transcript = result.get("transcriptions", [])
    # Normalize to a simple list of dicts for downstream steps
    normalized = []
    for word_info in transcript:
        normalized.append(
            {
                "start": word_info.get("start", ""),
                "end": word_info.get("duration", ""),  # Azure uses "duration"
                "text": word_info.get("text", ""),
                "speaker": word_info.get("speakerLabel", ""),
            }
        )
    return normalized


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: timestamped_transcript.py <job_id>", file=sys.stderr)
        sys.exit(1)
    job_id = sys.argv[1]
    ts_transcript = fetch_timestamped_transcript(job_id)
    print(ts_transcript)
