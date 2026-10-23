import os
from google.generativeai import GenerativeModel

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

model = GenerativeModel('gemini-1.5-pro')

def summarize_record(text):
    response = model.generate_content(text)
    return response.text