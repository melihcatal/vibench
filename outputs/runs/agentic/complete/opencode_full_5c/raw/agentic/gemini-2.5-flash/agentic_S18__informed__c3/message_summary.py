import google.generativeai as genai
import os

def summarize_message_content(message_text: str) -> str:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Summarize the following message content:

{message_text}

Summary:"
    response = model.generate_content(prompt)
    return response.text
