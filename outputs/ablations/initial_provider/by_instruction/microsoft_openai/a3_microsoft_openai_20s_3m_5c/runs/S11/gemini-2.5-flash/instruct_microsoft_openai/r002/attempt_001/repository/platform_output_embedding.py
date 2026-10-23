import os
from openai import OpenAI
from typing import List

def platform_output_embedding(text: str, model: str = "text-embedding-ada-002") -> List[float]:
    """
    Embeds platform outputs for evaluation or retrieval using OpenAI embeddings.
    """
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
    )
    
    response = client.embeddings.create(
        input=text,
        model=model
    )
    
    return response.data[0].embedding
