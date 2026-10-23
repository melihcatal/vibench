import os
import google.generativeai as genai

def summarize_text(text: str) -> str:
    """
    Calls Google's Generative AI to summarize long text.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Summarize the following text:\n\n{text}"
    response = model.generate_content(prompt)
    return response.text

