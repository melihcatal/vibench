import os
import google.generativeai as genai


def onboarding_summary(onboarding_state: Dict[str, Any]) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"Summarize the following onboarding state for a support agent:\n\n{onboarding_state}"
    response = model.generate_content(prompt)
    return response.text
