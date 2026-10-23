import openai
from typing import List, float

def platform_output_embedding(text: str) -> List[float]:
    client = openai.OpenAI()
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text,
    )
    return list(response.data[0].embedding)