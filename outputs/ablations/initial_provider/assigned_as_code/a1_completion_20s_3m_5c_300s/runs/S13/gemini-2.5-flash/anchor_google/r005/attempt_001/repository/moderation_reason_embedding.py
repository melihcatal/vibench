import os
from typing import List
from openai import OpenAI

def moderation_reason_embedding(reasons: List[str]) -> List[List[float]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Combine reasons into a single string or embed each reason separately
    # For this example, let's embed each reason separately.
    embeddings = []
    for reason in reasons:
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input=[reason]
        )
        embeddings.append(response.data[0].embedding)
    
    return embeddings
