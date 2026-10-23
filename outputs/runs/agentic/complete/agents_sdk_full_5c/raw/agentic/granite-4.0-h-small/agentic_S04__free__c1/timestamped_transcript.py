import os
import json
from speech_client import BatchSpeechClient
from speech_models import TimestampedTranscript

# ------------------------------------------------------------
# timestamped_transcript.py
# Retrieve word/segment timestamps from a completed transcription job
# ------------------------------------------------------------

def get_timestamped_transcript(job_id: str) -> TimestampedTranscript:
    """Fetch the timestamped transcript for a completed batch transcription job.

    Returns a TimestampedTranscript object containing segments with start/end times.
    """
    client = BatchSpeechClient()
    raw = client.get_transcription_results(job_id)
    return TimestampedTranscript.parse_obj(raw)

# Example usage (command line)
if __name__ == "__main__":
    import argparse, json
    parser = argparse.ArgumentParser(description="Get timestamps for a batch transcript.")
    parser.add_argument("job_id", help="Job ID from submit_transcription.")
    args = parser.parse_args()
    ts = get_timestamped_transcript(args.job_id)
    # Convert to simple list of dicts for readability
    output = [
        {
            "word": seg.word,
            "start": seg.start_time,
            "end": seg.end_time
        }
        for seg in ts.segments
    ]
    print(json.dumps(output, indent=2))
