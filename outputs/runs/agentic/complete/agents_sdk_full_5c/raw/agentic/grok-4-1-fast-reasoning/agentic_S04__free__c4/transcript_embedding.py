import os
import openai
from typing import List

def transcript_embedding(text: str) -> List[float]:
    """
    Embed transcript segments for semantic retrieval.
    """
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding