import os
from google.generativeai import GenerativeModel

model = GenerativeModel("gemini-pro")


def embed_output(text):
    response = model.generate_content(text)
    return response.embedding
