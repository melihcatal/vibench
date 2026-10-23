import google.generativeai as genai
import os

def embed_translation_segment(payload, config=None):
    config = config or {}
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('embedding-001')
    response = model.embed_content(model_name="embedding-001", content=payload["text"])
    return {
        "text": payload["text"],
        "embedding": response['embedding'],
    }
