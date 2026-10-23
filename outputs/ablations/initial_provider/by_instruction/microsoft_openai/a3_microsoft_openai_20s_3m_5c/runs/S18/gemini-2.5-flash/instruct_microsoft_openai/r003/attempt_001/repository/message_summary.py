import os
import google.generativeai as genai

def summarize_message(message_payload: str) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    
    prompt = f"Please summarize the following message payload:\n\n{message_payload}"
    response = model.generate_content(prompt)
    
    return response.text
