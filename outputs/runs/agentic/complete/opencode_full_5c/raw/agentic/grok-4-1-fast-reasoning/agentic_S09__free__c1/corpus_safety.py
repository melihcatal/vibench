import os
from typing import List
from openai import OpenAI


def check_corpus_safety(texts: List[str]) -> List[bool]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    if not texts:
        return []
    response = client.moderations.create(input=texts, model="text-moderation-latest")
    return [not result.flagged for result in response.results]
