import os
from google.generativeai import GenerativeModel

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

def audit_summary(audit_events):
    model = GenerativeModel(model_name='gemini-1.5-pro-latest', api_key=GOOGLE_API_KEY)
    summary = model.generate_content(audit_events)
    return summary