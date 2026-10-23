import google.generativeai as genai
import os
from typing import List

def embed_log_messages(log_messages: List[str]) -> List[List[float]]:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = "models/embedding-001"

    embeddings = []
    for message in log_messages:
        response = genai.embed_content(model=model, content=message)
        embeddings.append(response['embedding'])

    return embeddings
