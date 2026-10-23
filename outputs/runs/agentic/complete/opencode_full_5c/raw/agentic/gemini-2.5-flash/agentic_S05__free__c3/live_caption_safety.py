import google.generativeai as genai # Provider SDK import
import os

def check_safety(text: str):
    """Checks live transcript text for unsafe content using Google Generative AI (Gemini/PaLM API)."""
    # Ensure GOOGLE_API_KEY is set in environment variables
    try:
        genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    except KeyError:
        return "Error: GOOGLE_API_KEY environment variable not set."

    # Using a content moderation model, e.g., text-moderation-004 (example model ID)
    # The actual model ID might vary or be a safety setting within a larger model.
    # For this example, we'll simulate with a generic text model and prompt for safety.
    model = genai.GenerativeModel('gemini-pro') # Provider-specific model ID/family

    prompt = f"Is the following text safe and appropriate? Respond with 'safe' or 'unsafe'. Text: \""""{text}"""""

    try:
        response = model.generate_content(prompt)
        # Assuming the model returns a simple 'safe' or 'unsafe'
        return response.text.strip().lower()
    except Exception as e:
        return f"Error checking safety: {e}"
