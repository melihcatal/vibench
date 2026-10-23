import openai
import os
from typing import List

client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def ocr_embedding(sections: List[str]) -> List[list[float]]:
    """
    Embed extracted document sections for semantic retrieval.
    """
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=sections
    )
    return [data.embedding for data in response.data]
