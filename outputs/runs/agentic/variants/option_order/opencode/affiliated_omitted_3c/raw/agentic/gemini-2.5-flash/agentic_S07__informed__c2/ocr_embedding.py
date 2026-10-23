import os
from openai import OpenAI


def ocr_embedding(text: str, model: str = "text-embedding-ada-002") -> list[float]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY must be set in environment variables")

    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding
