from speech_client import post
from speech_models import SummaryRequest


def archive_summary(transcript: str) -> dict:
    req = SummaryRequest(transcript=transcript)
    return post(
        "/responses",
        {"model": "gpt-4.1-mini", "input": f"Summarize for archive: {req.transcript}"},
    )
