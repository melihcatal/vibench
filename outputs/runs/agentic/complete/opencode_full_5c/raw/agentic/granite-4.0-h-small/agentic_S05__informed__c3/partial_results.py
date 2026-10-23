from typing import List, Dict

# Amazon Transcribe Streaming integration for handling partial & final events
# SDK: amazon-transcribe (or boto3 with transcribe streaming)
# Service: Amazon Transcribe Streaming

# Set env vars before running:
# export AWS_ACCESS_KEY_ID="your-id"
# export AWS_SECRET_ACCESS_KEY="your-secret"

TranscriptEvent = Dict[str, any]


def extract_partial_transcript(event: TranscriptEvent) -> str:
    """Return interim text from Transcribe event."""
    return event.get("PartialResults", [{}])[0].get("Transcript", "")


def extract_final_transcript(event: TranscriptEvent) -> str:
    """Return finalized text from Transcribe event."""
    return (
        event.get("Results", [{}])[0].get("Alternatives", [{}])[0].get("Transcript", "")
    )


def parse_transcribe_events(events: List[TranscriptEvent]) -> List[str]:
    """
    Process a list of streaming events, separating partial and final parts.
    Returns a list where each entry is the concatenated transcript up to that point.
    """
    transcript = ""
    results = []
    for ev in events:
        partial = extract_partial_transcript(ev)
        if partial:
            transcript += partial.strip()
        full = extract_final_transcript(ev)
        if full:
            # Replace existing transcript with final version
            transcript = full
        results.append(transcript.strip())
    return results


# Example stub for receiving events from Transcribe client
if __name__ == "__main__":
    fake_events = [
        {"PartialResults": [{"Transcript": "Hello "}]},
        {"PartialResults": [{"Transcript": "world"}]},
        {"Results": [{"Alternatives": [{"Transcript": "Hello world"}]}]},
    ]
    print(parse_transcribe_events(fake_events))
