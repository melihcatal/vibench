import os
import google.generativeai as genai

# Configure the Google Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def summarize_onboarding_state(onboarding_data: dict) -> dict:
    if not genai.get_default_model():
        return {"error": "Google Gemini API key not configured or invalid."}

    model = genai.GenerativeModel('gemini-pro') # Using a specific model identifier

    prompt = f"""
    Summarize the following user onboarding state for a support agent. 
    Highlight any incomplete steps, potential issues, or areas requiring attention. 
    Keep the summary concise and actionable.

    User Onboarding Data: 
    {{onboarding_data}}
    """

    try:
        response = model.generate_content(prompt)
        summary_text = response.text.strip()
        return {"summary": summary_text, "raw_response": response.to_dict()}
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY environment variable)
    # example_data = {
    #     "user_id": "user123",
    #     "email": "user@example.com",
    #     "registration_complete": True,
    #     "email_verified": False,
    #     "profile_completed": False,
    #     "payment_info_added": True,
    #     "welcome_email_sent": True,
    #     "last_login": "2023-10-27T10:00:00Z"
    # }
    # summary = summarize_onboarding_state(example_data)
    # print(summary)
    pass
