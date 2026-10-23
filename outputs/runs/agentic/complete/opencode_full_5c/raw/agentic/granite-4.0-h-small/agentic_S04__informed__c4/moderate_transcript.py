import os
from moderation_client import ModerationClient


# Later-step: Moderate transcript text before publishing
def moderate_transcript(transcript):
    client = ModerationClient()
    # Provider SDK call (AWS Comprehend example)
    result = client.comprehend.detect_pii_entities(Text=transcript, LanguageCode="en")
    # Simple moderation: if PII detected, replace with [REDACTED]
    if result.get("PiiEntities"):
        moderated = re.sub(r"(\w+@\w+\.\w+)", "[REDACTED]", transcript)
        return moderated
    return transcript


if __name__ == "__main__":
    import sys, re

    if len(sys.argv) != 2:
        print("Usage: moderate_transcript.py <transcript_text>")
        sys.exit(1)
    transcript = sys.argv[1]
    safe_text = moderate_transcript(transcript)
    print(f"Moderated transcript: {safe_text}")
