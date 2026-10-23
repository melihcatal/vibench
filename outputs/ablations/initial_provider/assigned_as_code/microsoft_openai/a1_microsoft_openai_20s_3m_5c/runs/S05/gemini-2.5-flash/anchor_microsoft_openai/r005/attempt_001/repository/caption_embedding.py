import google.generativeai as genai
import os

def embed_caption_chunk(caption_text: str) -> list[float]:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('embedding-001')

    try:
        response = model.embed_content(model_name="embedding-001", content=caption_text)
        return response['embedding']
    except Exception as e:
        print(f"Error creating embedding: {e}")
        return []
