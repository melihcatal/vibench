import google.generativeai as genai
import os

def stream_completion(prompt: str):
    """
    Streams partial output tokens from a hosted LLM (Google Gemini).
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    for chunk in model.generate_content(prompt, stream=True):
        yield chunk.text
