import os
import google.generativeai as genai
from typing import List


def moderation_reason_embedding(reasons: List[str]) -> List[List[float]]:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")  # Using gemini-pro for embedding

    # The embedding model is actually different for embeddings in GenAI.
    # Using the specific embedding model here.
    embedding_model = "models/embedding-001"

    embeddings = []
    for reason in reasons:
        response = genai.embed_content(model=embedding_model, content=reason)
        embeddings.append(response["embedding"])

    return embeddings
