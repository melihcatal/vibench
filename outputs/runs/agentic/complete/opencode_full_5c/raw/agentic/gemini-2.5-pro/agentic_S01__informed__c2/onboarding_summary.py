import os
import json
import google.generativeai as genai


def summarize_onboarding_state(onboarding_data: dict) -> str:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-pro")

    prompt = f"""
    Summarize the following user onboarding state for a support agent.
    Focus on key milestones, identify any potential issues, and provide a concise overview.

    Onboarding Data:
    {json.dumps(onboarding_data, indent=2)}
    """

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while generating the summary: {e}"
