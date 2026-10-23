import cohere
import os

def ocr_embedding(sections: list[str]) -> list[list[float]]:
    client = cohere.Client(os.getenv('COHERE_API_KEY'))
    response = client.embed(
        texts=sections,
        model='embed-english-v3.0'
    )
    return response.embeddings
