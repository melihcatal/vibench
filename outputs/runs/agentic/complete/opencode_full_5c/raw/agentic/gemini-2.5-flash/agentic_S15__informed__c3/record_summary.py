import os
import google.generativeai as genai


def summarize_record(text_content: str) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")  # Google Gemini API
    response = model.generate_content(f"Summarize the following text: {text_content}")
    return response.text
