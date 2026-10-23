from speech_client import post
from speech_models import ModerationRequest


def moderate_transcript(text: str) -> dict:
    req = ModerationRequest(text=text)
    return post("/moderations", {"model": "omni-moderation-latest", "input": req.text})
