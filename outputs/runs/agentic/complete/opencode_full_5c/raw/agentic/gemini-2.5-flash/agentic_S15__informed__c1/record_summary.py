import google.generativeai as genai
import os


def summarize_record(text_content: str):
    # Ensure GOOGLE_API_KEY environment variable is set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(f"Summarize the following text: {text_content}")
    return {"status": "success", "summary": response.text}
