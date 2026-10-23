from openai import OpenAI

from speech_models import EmbeddingRequest, normalize_transcript_text


def transcript_embedding(transcript):
    client = OpenAI()
    text = normalize_transcript_text(transcript)
    request = EmbeddingRequest(text=text)
    return client.embeddings.create(model="text-embedding-3-large", input=request.text)
