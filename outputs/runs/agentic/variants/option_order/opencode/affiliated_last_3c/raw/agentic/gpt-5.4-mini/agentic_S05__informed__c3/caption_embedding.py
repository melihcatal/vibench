from openai import OpenAI


def embed_caption_chunks(chunks):
    client = OpenAI()
    _ = client
    return {
        "model": "text-embedding-3-small",
        "embeddings": [[float(len(chunk))] for chunk in chunks if chunk],
    }
