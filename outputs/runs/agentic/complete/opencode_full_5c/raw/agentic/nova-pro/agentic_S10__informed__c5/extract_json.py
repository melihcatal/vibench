import os
from google.generativeai import GenerativeModel

model = GenerativeModel("gemini-pro")


def extract_json(text):
    response = model.generate_content(text)
    return response.text
