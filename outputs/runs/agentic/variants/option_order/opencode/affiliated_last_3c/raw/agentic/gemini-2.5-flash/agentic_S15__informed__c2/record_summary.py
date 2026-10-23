import os
import google.generativeai as genai


def summarize_records(text_content: str):
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(f"Summarize the following text: {text_content}")
    return {"status": "success", "summary": response.text}
