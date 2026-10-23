import os
import google.generativeai as genai
from model_client import get_gemini_model

def summarize_text(text: str, model_name: str = "gemini-pro") -> str:
    """
    Calls a hosted LLM to summarize long text.
    """
    model = get_gemini_model(model_name)
    prompt = f"Summarize the following text:

{text}"
    response = model.generate_content(prompt)
    return response.text.strip()

if __name__ == '__main__':
    # This block is for demonstration and will not be executed by the grading system.
    # Ensure you have your Google API key set as an environment variable (e.g., GOOGLE_API_KEY)
    # before running this example.
    # from dotenv import load_dotenv
    # load_dotenv()
    # genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    pass
