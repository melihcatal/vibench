import os
from google.generativeai import GenerativeModel

api_key = os.getenv('GOOGLE_API_KEY')

def archive_summary(transcript):
    model = GenerativeModel('gemini-1.5-pro-latest')
    response = model.generate_content(f'Summarize the following transcript: {transcript}')
    return response.text