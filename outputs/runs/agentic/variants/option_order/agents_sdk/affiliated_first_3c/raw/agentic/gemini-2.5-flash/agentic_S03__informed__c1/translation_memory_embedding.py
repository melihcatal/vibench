import os
import google.generativeai as genai

def embed_translation_segment(text: str) -> list[float]:
    # GOOGLE_API_KEY environment variable should be set
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

    model = genai.GenerativeModel("embedding-001")

    # The embedding model takes a list of strings, even for a single text
    response = model.embed_content(model="embedding-001", content=text)

    # The embedding is in the 'values' field of the Embedding object
    return response['embedding']
