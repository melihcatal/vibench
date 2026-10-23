import os
import google.generativeai as genai


def onboarding_summary(onboarding_state: dict, config=None) -> dict:
    config = config or {}
    # Configure the Google Generative AI client
    # Uses GOOGLE_API_KEY environment variable by default
    genai.configure(api_key=config.get("google_api_key") or os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro') # Using a capable model like gemini-pro

    # Construct a prompt for summarization
    prompt = f"Summarize the following user onboarding state for a support agent, highlighting key progress and any potential issues:\n\n{onboarding_state}"

    response = model.generate_content(prompt)

    return {"summary": response.text}
