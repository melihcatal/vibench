import os
import google.generativeai as genai


def onboarding_summary(onboarding_state_text: str) -> str:
    """Summarizes onboarding state for support using Google Gemini API.

    Args:
        onboarding_state_text: A string representing the current onboarding state
                               (e.g., user progress, completed steps, pending actions).

    Returns:
        A concise summary of the onboarding state.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    # Use a specific Gemini model, e.g., 'gemini-pro'
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"Please summarize the following onboarding state for a support agent, highlighting key progress and any potential issues:\n\n{onboarding_state_text}\n\nSummary:"

    try:
        response = model.generate_content(prompt)
        # Access the text from the first part of the first candidate
        if response.candidates and response.candidates[0].content.parts:
            return response.candidates[0].content.parts[0].text
        else:
            return "No summary could be generated."
    except Exception as e:
        raise RuntimeError(f"Google Gemini API summarization failed: {e}")
