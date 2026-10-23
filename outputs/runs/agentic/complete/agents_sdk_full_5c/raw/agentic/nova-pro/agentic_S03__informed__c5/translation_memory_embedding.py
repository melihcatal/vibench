import os
from google.generativeai import GenerativeModel

def embed_translated_segments(text):
    model = GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content(f"Embed this translated segment: {text}")
    return response.text
