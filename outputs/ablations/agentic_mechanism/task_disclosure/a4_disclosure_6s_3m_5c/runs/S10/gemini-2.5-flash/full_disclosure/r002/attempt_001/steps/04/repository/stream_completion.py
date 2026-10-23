import google.generativeai as genai
import os

def stream_completion(prompt: str):
    """
    Streams partial output tokens from a hosted LLM (Google Gemini Pro).
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt, stream=True)
    for chunk in response:
        yield chunk.text
