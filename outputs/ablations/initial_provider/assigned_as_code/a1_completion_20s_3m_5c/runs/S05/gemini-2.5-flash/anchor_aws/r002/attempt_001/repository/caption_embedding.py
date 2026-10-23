import os
import google.generativeai as genai

def embed_caption_chunk(caption_chunk: str) -> list[float]:
    # Configure the Google Generative AI client
    # Ensure GOOGLE_API_KEY environment variable is set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('embedding-001')

    response = model.embed_content(model_id='embedding-001', content=caption_chunk)
    return response['embedding']
