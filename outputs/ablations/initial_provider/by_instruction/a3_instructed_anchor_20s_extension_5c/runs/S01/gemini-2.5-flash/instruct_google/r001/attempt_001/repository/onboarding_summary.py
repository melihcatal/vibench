import os
import google.generativeai as genai

# Configure Gemini API with your API key
# Ensure GOOGLE_API_KEY environment variable is set.
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def onboarding_summary(onboarding_data):
    """
    Summarizes onboarding state for support using the Google Gemini API.
    The `onboarding_data` should be a string or a structured text representing
    the user's onboarding progress and relevant information.
    """
    try:
        model = genai.GenerativeModel('gemini-pro') # Using a general-purpose model

        prompt = f"""Please summarize the following onboarding data for a support agent. 
        Highlight key milestones, any incomplete steps, and potential issues:

        {onboarding_data}

        Summary:"""

        response = model.generate_content(prompt)
        return {"summary": response.text, "message": "Onboarding summary generated."}
    except Exception as e:
        return {"error": str(e), "message": "Failed to generate onboarding summary."}
