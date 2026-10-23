import google.generativeai as genai
import os

def get_caption_embedding(text: str) -> list[float]:
    # Ensure the API key is set as an environment variable
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('text-embedding-004')

    response = model.embed_content(model='text-embedding-004', content=text)
    return response['embedding']
