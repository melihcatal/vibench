import os
from typing import List
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed_output(text: str) -> List[float]:
    \"\"\"Generate embedding for model output using OpenAI.\"\"\"
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return list(response.data[0].embedding)