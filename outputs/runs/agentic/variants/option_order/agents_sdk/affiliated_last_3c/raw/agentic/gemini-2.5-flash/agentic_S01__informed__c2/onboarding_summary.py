import os
import google.generativeai as genai

def summarize_onboarding_state(user_id: str, onboarding_steps: list[str]) -> str:
    """
    Summarizes onboarding state for support using the Google Gemini API.
    
    Requires GOOGLE_API_KEY environment variable.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""Summarize the onboarding state for user ID {user_id}.
The user has completed the following steps:
{", ".join(onboarding_steps)}

Provide a concise summary suitable for a support agent to quickly understand the user's progress.
"""
    
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    # Example Usage (Requires GOOGLE_API_KEY environment variable)
    # user_id_example = "user-12345"
    # completed_steps = [
    #     "Email Verified",
    #     "Profile Created",
    #     "Payment Method Added",
    #     "Tutorial Completed"
    # ]
    # try:
    #     summary = summarize_onboarding_state(user_id_example, completed_steps)
    #     print(f"Onboarding Summary for {user_id_example}:\n{summary}")
    # except ValueError as e:
    #     print(f"Configuration error: {e}")
    # except Exception as e:
    #     print(f"Error summarizing onboarding state: {e}")
    pass
