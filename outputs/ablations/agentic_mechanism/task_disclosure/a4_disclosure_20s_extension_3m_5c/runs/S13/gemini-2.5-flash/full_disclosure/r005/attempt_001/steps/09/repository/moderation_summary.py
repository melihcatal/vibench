import google.generativeai as genai
import os

def summarize_moderation_decisions(decisions: list[str]) -> str:
    """
    Summarizes moderation decisions using Google's Generative AI.

    Args:
        decisions: A list of strings, where each string represents a moderation decision.

    Returns:
        A single string containing the summary of the moderation decisions.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt = "Summarize the following moderation decisions:
"
    for i, decision in enumerate(decisions):
        prompt += f"{i+1}. {decision}\n"

    response = model.generate_content(prompt)
    return response.text
