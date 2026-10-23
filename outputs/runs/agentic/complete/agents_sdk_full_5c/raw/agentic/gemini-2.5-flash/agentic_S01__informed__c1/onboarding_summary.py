import os
import google.generativeai as genai

def summarize_onboarding_state(onboarding_data: str) -> dict:
    """
    Summarizes onboarding state for support using the Google Gemini API.
    Requires GOOGLE_API_KEY to be set.
    """
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise EnvironmentError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)

    try:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Summarize the following user onboarding state for a support agent:

{onboarding_data}"
        response = model.generate_content(prompt)
        
        if response.text:
            return {"summary": response.text}
        else:
            return {"error": "No summary generated or empty response."}
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    # Example usage:
    # export GOOGLE_API_KEY="YOUR_GEMINI_API_KEY"
    # user_onboarding_info = """
    # User ID: user123
    # Email: user@example.com
    # Registration Date: 2023-10-26
    # Last Login: 2023-10-26
    # Profile Steps Completed: Basic Info, Email Verified
    # Profile Steps Pending: Payment Method, Two-Factor Authentication
    # Recent Activity: Viewed pricing page, started trial.
    # Notes: User contacted support regarding pricing plans.
    # """
    # summary_result = summarize_onboarding_state(user_onboarding_info)
    # print(summary_result)
    pass
