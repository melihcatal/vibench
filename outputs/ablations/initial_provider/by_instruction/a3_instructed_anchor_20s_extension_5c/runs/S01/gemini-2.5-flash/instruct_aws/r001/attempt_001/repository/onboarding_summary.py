import google.generativeai as genai
import os

def onboarding_summary(onboarding_data):
    # Configure the Gemini API client
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Use a specific Gemini model for text generation
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"Summarize the following user onboarding data: {onboarding_data}"

    response = model.generate_content(prompt)

    return response.text
