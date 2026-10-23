import os
from openai import OpenAI
from typing import List


def embed_script(
    script_text: str, model: str = "text-embedding-3-small"
) -> List[float]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    response = client.embeddings.create(input=[script_text], model=model)

    return response.data[0].embedding
