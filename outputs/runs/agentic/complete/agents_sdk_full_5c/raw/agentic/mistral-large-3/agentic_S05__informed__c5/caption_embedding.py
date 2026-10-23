import os
from google.generativeai import GenerativeModel

def embed_caption_chunk(text_chunk):
    model = GenerativeModel(model_name="models/text-embedding-004")
    result = model.embed_content(content=text_chunk)
    return result.embedding