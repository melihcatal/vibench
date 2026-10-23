import os
import google.generativeai as genai

def summarize_moderation_decisions(decisions: list[dict]) -> str:
    """
    Summarize moderation decisions using Google Gemini API.
    """
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel('gemini-pro')

    prompt = """
    Summarize the following moderation decisions. Highlight any text that was flagged and the reasons.

    Moderation Decisions:
    """

    for decision in decisions:
        prompt += f"Text: {decision['text']}\n"
        for result in decision['moderation_results']:
            prompt += f"  - Category: {result['category']}, Severity: {result['severity']}\n"
        prompt += "\n"

    response = model.generate_content(prompt)
    return response.text

