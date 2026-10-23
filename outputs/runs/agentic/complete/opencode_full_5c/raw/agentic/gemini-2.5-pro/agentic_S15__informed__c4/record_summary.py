import os
import google.generativeai as genai


def summarize_text(text: str) -> str:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"Please provide a concise summary of the following text:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text
