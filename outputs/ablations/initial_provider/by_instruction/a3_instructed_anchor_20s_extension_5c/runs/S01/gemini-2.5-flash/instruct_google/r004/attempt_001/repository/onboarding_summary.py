# [LATER-STEP] onboarding_summary.py - Summarize onboarding state for support
# Provider: Google Cloud Generative AI (Gemini/PaLM API)

import os
import google.generativeai as genai

def summarize_onboarding_state(onboarding_data: dict) -> str:
    # Configure the Gemini API client
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Choose a model
    model = genai.GenerativeModel('gemini-pro') # Using gemini-pro as an example

    # Construct a prompt for summarization
    prompt = f"Summarize the following onboarding state for a support agent: {onboarding_data}"

    # Generate content
    response = model.generate_content(prompt)
    return response.text
