import os
from openai import AzureOpenAI
from typing import List

def embed_transcript_segments(text_segments: List[str], model: str = "text-embedding-ada-002") -> List[List[float]]:
    client = AzureOpenAI(
        api_key=os.environ.get("AZURE_OPENAI_API_KEY"),
        api_version="2023-05-15",
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT")
    )

    embeddings = []
    for segment in text_segments:
        response = client.embeddings.create(
            input=segment,
            model=model
        )
        embeddings.append(response.data[0].embedding)
    
    return embeddings
