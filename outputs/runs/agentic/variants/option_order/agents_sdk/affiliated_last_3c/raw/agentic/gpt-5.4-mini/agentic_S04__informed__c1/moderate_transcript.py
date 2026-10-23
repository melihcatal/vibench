import os

from openai import OpenAI

from speech_models import TranscriptArtifact, join_segments


OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def moderate_transcript(artifact: TranscriptArtifact) -> dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    text = artifact.transcript or join_segments(artifact.segments)
    moderation = client.moderations.create(model=OPENAI_MODERATION_MODEL, input=text)
    result = moderation.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
        "input": text,
    }
