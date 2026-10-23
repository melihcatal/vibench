import os
import google.generativeai as genai

def onboarding_summary(onboarding_state: dict) -> str:
    # Configure the generative AI client
    # The GOOGLE_API_KEY environment variable should be set for authentication.
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    # Choose a model
    model = genai.GenerativeModel('gemini-pro') # Using gemini-pro for text generation

    prompt = f"Summarize the following user onboarding state for a support agent, highlighting key completed steps and any pending actions:\n\n{onboarding_state}"

    response = model.generate_content(prompt)
    return response.text
