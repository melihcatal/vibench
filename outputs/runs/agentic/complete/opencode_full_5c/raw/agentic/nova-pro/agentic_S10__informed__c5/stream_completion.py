import os
from google.generativeai import GenerativeModel

model = GenerativeModel("gemini-pro")


def stream_completion(text):
    response = model.generate_content_stream(text)
    for chunk in response:
        yield chunk.text
