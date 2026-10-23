import google.generativeai as genai
import os
from identity_models import OnboardingSummaryRequest, OnboardingSummaryResponse

# Ensure GOOGLE_API_KEY environment variable is set
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def onboarding_summary(request: OnboardingSummaryRequest) -> OnboardingSummaryResponse:
    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Summarize the onboarding state for user {request['user_id']}. " \
                 f"Completed steps: {', '.join(request['onboarding_steps_completed'])}. " \
                 f"Profile text: {request['profile_text']}. " \
                 "Provide a concise summary for support personnel."
        
        response = model.generate_content(prompt)
        
        if response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
            summary_text = response.candidates[0].content.parts[0].text
            return {"summary": summary_text}
        else:
            raise RuntimeError("Failed to generate summary: No content in response.")

    except Exception as e:
        raise RuntimeError(f"Failed to summarize onboarding state: {e}")

