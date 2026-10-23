import os
import google.generativeai as genai

def record_summary(text_content: str, config: dict = None):
    config = config or {}
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY", config.get("google_api_key")))
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Summarize the following text:\n\n{text_content}"
    response = model.generate_content(prompt)
    return {"summary": response.text}
