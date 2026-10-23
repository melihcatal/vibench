from model_models import EmbeddingResult
from openai import OpenAI
import os


def embed_output(texts):
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    resp = client.embeddings.create(model="text-embedding-3-small", input=texts)
    vectors = [item.embedding for item in resp.data]
    return EmbeddingResult(vectors=vectors, model="text-embedding-3-small")
