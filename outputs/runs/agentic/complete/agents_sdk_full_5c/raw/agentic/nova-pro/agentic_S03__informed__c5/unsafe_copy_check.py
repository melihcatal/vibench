import os
from google.generativeai import GenerativeModel

def check_unsafe_content(text):
    model = GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content(f"Check for unsafe content in this translation: {text}")
    return response.text
