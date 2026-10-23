from openai import OpenAI
import os


def output_embedding(text: str) -> list[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small"), input=text)
    return response.data[0].embedding
