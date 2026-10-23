import google.generativeai as genai
import os

def summarize_onboarding_state(onboarding_data: dict) -> str:
    """
    Summarizes the onboarding state for support using Google Generative AI.
    
    Args:
        onboarding_data: A dictionary containing onboarding information.
                         Example: {"user_id": "123", "steps_completed": ["email_verified", "profile_created"], "last_activity": "2023-10-27"}
    
    Returns:
        A string summarizing the onboarding state.
    """
    
    # Configure the Google Generative AI client
    # Ensure GOOGLE_API_KEY is set in your environment variables
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Initialize the Generative Model
    model = genai.GenerativeModel('gemini-pro')

    # Create a prompt for the model
    prompt = f"Summarize the following user onboarding state for support purposes:
{onboarding_data}"

    # Generate content
    response = model.generate_content(prompt)

    return response.text
