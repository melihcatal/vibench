import os
import google.generativeai as genai

# GOOGLE_API_KEY environment variable should be set

def summarize_text_chunk(text_chunk: str, model_name: str = "gemini-pro") -> str:
    """Summarizes a given text chunk using the Google Gemini API."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable is not set.")
        return "Error: Gemini API key not configured."

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    prompt = f"Summarize the following meeting transcript chunk:

{text_chunk}

Summary:"

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating summary with Gemini API: {e}")
        return f"Error: {str(e)}"
