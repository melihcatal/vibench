import google.generativeai
import os

def summarize_message(message: str) -> str:
    """
    Summarizes message processing results using Google's Generative AI.
    """
    # Ensure GOOGLE_API_KEY is set in environment variables
    # For local development, you might set it directly or use a .env file.
    # In a production environment, use secure methods for API key management.
    try:
        google.generativeai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    except KeyError:
        return "Error: GOOGLE_API_KEY environment variable not set."

    model = google.generativeai.GenerativeModel('gemini-pro')
    
    prompt = f"Summarize the following message processing result: {message}"
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error summarizing message: {e}"

