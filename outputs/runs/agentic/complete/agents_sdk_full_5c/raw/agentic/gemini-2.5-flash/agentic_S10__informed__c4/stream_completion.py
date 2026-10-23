import google.generativeai as genai
import os
from model_client import get_gemini_client

def stream_completion(prompt: str):
    """
    Streams partial output tokens from a hosted LLM (Gemini).
    """
    client = get_gemini_client()
    model = client.GenerativeModel("gemini-pro")
    
    responses = model.generate_content(prompt, stream=True)
    
    print("Streaming LLM response:")
    full_response = ""
    for chunk in responses:
        print(chunk.text, end='')
        full_response += chunk.text
    print("\n") # Add a newline at the end
    return full_response

if __name__ == '__main__':
    os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY" # Replace with your actual key or set it in your environment
    
    test_prompt = "Tell me a short story about a brave knight and a dragon."
    stream_completion(test_prompt)
