from openai import OpenAI
from speech_client import load_config


def transcript_embedding(segments: list[str]) -> list[list[float]]:
    client = OpenAI(api_key=load_config().api_key or "")
    response = client.embeddings.create(model="text-embedding-3-large", input=segments)
    return [item.embedding for item in response.data]
