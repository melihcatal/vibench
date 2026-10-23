import os
import google.generativeai as genai

def summarize_stored_asset_content(text_content: str) -> str:
    # Google Cloud Generative AI setup
    # Ensure GOOGLE_API_KEY is set in environment variables
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")

    genai.configure(api_key=google_api_key)

    model = genai.GenerativeModel('gemini-pro') # Using gemini-pro for summarization
    prompt = f"Summarize the following text:\n\n{text_content}"

    response = model.generate_content(prompt)
    return response.text
