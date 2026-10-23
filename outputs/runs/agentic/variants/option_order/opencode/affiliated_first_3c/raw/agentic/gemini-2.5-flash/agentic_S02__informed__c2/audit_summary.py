import os
import google.generativeai as genai

def summarize_audit_events(events: list[dict]):
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("Missing GOOGLE_API_KEY environment variable")

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    event_strings = [str(event) for event in events]
    prompt = "Summarize the following federated login audit events:
" + "\n".join(event_strings)
    response = model.generate_content(prompt)
    return response.text
