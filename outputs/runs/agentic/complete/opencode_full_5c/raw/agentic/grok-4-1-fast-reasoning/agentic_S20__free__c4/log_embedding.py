import os
import openai
from typing import List


def embed_log_message(message: str) -> List[float]:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(input=message, model="text-embedding-3-small")
    return [float(x) for x in response.data[0].embedding]
