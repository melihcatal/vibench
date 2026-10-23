from typing import List

from openai import OpenAI


def platform_output_embedding(text: str, model: str = "text-embedding-3-small") -> List[float]:
    client = OpenAI(api_key=__import__("os").environ.get("OPENAI_API_KEY", ""))
    response = client.embeddings.create(model=model, input=text)
    return list(response.data[0].embedding)
