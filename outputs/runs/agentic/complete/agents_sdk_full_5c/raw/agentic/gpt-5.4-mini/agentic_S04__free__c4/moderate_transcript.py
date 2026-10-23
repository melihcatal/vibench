from __future__ import annotations

from typing import Dict, List

from speech_client import OPENAI_TEXT_MODEL, SpeechClientFactory


def moderate_transcript(segments: List[Dict[str, str]]) -> Dict[str, str]:
    client = SpeechClientFactory.create()
    transcript = "\n".join(segment.get("text", "") for segment in segments)
    response = client.moderations.create(model="omni-moderation-latest", input=transcript)
    result = response.results[0]
    return {"flagged": str(result.flagged), "categories": str(result.categories), "model": OPENAI_TEXT_MODEL}
