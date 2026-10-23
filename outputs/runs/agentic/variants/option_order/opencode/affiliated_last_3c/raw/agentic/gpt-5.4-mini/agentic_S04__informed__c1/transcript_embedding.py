from openai import OpenAI

from speech_models import normalize_segments


def transcript_embedding(payload: dict) -> list[list[float]]:
    client = OpenAI()
    vectors = []
    for segment in normalize_segments(payload):
        text = segment.get("text", "")
        if text:
            response = client.embeddings.create(
                model="text-embedding-3-small", input=text
            )
            vectors.append(response.data[0].embedding)
    return vectors
