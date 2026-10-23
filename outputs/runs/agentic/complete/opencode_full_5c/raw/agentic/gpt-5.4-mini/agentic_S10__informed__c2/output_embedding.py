from openai import OpenAI
import os


def output_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(model=model, input=text)
    return response.data[0].embedding
