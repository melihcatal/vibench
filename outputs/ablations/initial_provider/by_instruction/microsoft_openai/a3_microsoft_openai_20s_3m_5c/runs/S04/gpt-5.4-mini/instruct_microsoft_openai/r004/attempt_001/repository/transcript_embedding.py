from openai import OpenAI

from speech_client import load_config


def transcript_embedding(segments):
    config = load_config("openai")
    client = OpenAI(api_key=config.api_key)
    texts = [segment if isinstance(segment, str) else segment.get("text", "") for segment in segments]
    return client.embeddings.create(model="text-embedding-3-small", input=texts).model_dump()
