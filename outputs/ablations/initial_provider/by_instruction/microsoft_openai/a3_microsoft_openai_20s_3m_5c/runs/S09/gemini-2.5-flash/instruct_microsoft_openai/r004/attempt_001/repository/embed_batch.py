import openai
import os

def embed_batch(texts: list[str]) -> list[list[float]]:
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.embeddings.create(
        input=texts,
        model="text-embedding-ada-002"
    )
    return [item.embedding for item in response.data]
