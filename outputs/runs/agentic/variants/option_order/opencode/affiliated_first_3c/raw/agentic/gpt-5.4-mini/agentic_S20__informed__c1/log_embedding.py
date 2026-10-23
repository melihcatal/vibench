import os
from typing import List

from openai import OpenAI


def log_embedding(messages: List[str]) -> list:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.embeddings.create(model="text-embedding-3-large", input=messages)
    return [item.embedding for item in response.data]


if __name__ == "__main__":
    log_embedding([])
