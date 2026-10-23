import openai
import os
from typing import List

openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def log_embedding(message: str) -> List[float]:
    response = openai_client.embeddings.create(
        input=message, model="text-embedding-3-small"
    )
    return response.data[0].embedding
