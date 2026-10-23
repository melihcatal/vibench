import os

from openai import OpenAI

from speech_models import TranscriptArtifact, join_segments


OPENAI_EMBEDDING_MODEL = "text-embedding-3-large"


def transcript_embedding(artifact: TranscriptArtifact) -> list[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    text = artifact.transcript or join_segments(artifact.segments)
    response = client.embeddings.create(model=OPENAI_EMBEDDING_MODEL, input=text)
    return list(response.data[0].embedding)
