import os
from google.generativeai import GenerativeModel

def summarize_quality_issues(text):
    model = GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content(f"Summarize quality issues in this translation: {text}")
    return response.text
