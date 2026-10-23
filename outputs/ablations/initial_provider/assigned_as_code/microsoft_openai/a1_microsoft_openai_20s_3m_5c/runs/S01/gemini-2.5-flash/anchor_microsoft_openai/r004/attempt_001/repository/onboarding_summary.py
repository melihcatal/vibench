import os
import google.generativeai as genai
from identity_models import OnboardingSummaryRequest

def onboarding_summary(payload: OnboardingSummaryRequest) -> dict:
    # Google Generative AI (Gemini API) initialization
    # Ensure GOOGLE_API_KEY environment variable is set
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    # Choose a generative model
    model = genai.GenerativeModel('gemini-pro') # Using gemini-pro for text generation/summarization

    # Construct the prompt for summarization
    onboarding_info = f"User ID: {payload.user_id}\n"
    onboarding_info += f"Onboarding steps completed: {', '.join(payload.onboarding_steps_completed)}\n"
    if payload.profile_text:
        onboarding_info += f"User profile text: {payload.profile_text}\n"

    prompt = f"Summarize the following user onboarding state for a support agent, highlighting key information and next steps if any:\n\n{onboarding_info}"

    # Generate the summary
    try:
        response = model.generate_content(prompt)
        summary_text = response.text
    except Exception as e:
        summary_text = f"Error generating summary: {str(e)}"

    return {
        "user_id": payload.user_id,
        "onboarding_summary": summary_text
    }
