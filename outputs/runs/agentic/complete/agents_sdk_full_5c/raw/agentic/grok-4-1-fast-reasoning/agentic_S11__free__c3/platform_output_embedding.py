import os
import cohere

def platform_output_embedding(output: str) -> list[float]:
    client = cohere.Client(os.getenv("COHERE_API_KEY"))
    response = client.embed(
        texts=[output],
        model="embed-english-v3.0"
    )
    return response.embeddings[0]
