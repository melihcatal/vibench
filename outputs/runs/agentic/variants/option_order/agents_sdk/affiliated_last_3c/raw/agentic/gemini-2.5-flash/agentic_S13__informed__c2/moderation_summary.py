import os
import google.generativeai as genai

def summarize_moderation_decisions(decisions: list) -> str:
    """
    Summarizes moderation decisions using the Google Gemini API.
    `decisions` is a list of dictionaries, where each dict represents a moderation decision.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""Review the following moderation decisions and provide a concise summary, highlighting any patterns or critical issues:

{decisions}

Summary:"""

    response = model.generate_content(prompt)
    return response.text
