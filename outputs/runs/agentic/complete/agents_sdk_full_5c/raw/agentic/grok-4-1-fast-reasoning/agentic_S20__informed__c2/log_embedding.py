import os
from typing import List
from openai import OpenAI

def log_embedding(text: str) -> List[float]:
    \"\"\"Embed selected log messages for semantic retrieval using OpenAI.\"\"\"
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.embeddings.create(
        model='text-embedding-3-small',
        input=text
    )
    return response.data[0].embedding
