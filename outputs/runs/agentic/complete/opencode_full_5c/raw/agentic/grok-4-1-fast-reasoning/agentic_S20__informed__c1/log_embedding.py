import openai
import os
from typing import List

openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def embed_log_messages(messages: List[str]) -> List[list]:
    embeddings = []
    for msg in messages:
        response = openai_client.embeddings.create(
            model="text-embedding-3-small", input=msg
        )
        embeddings.append(response.data[0].embedding)
    return embeddings
