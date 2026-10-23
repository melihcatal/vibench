import os
from openai import OpenAI

def get_embedding(text: str, model: str = "text-embedding-ada-002") -> list[float]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    if not os.environ.get("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable must be set.")

    text = text.replace("\n", " ")
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding
