from openai import OpenAI

from speech_models import caption_chunks_to_text, CaptionChunk


def caption_embedding(chunks: list[CaptionChunk]):
    client = OpenAI()
    text = caption_chunks_to_text(chunks)
    response = client.embeddings.create(model="text-embedding-3-small", input=text)
    return response.data[0].embedding
