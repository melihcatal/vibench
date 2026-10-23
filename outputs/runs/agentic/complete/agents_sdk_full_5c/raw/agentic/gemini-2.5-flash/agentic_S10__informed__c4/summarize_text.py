import google.generativeai as genai
import os
from model_client import get_gemini_client

def summarize_text(text: str) -> str:
    """
    Calls a hosted LLM (Gemini) to summarize long text.
    """
    client = get_gemini_client()
    model = client.GenerativeModel("gemini-pro")
    
    prompt = f"Please summarize the following text:

{text}"
    response = model.generate_content(prompt)
    
    return response.text

if __name__ == '__main__':
    # This is for local testing and demonstration.
    # In a real application, you would load this from an environment variable or secure config.
    os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY" # Replace with your actual key or set it in your environment
    
    long_text = "The quick brown fox jumps over the lazy dog. This is a very long sentence that needs to be summarized. It contains many words and phrases that can be condensed into a shorter form for easier reading and comprehension."
    summary = summarize_text(long_text)
    print(f"Original Text: {long_text}\n")
    print(f"Summary: {summary}")
