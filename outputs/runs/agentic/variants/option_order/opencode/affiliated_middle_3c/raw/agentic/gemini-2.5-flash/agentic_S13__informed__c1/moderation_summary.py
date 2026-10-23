import os
from typing import List
import google.generativeai as genai


def summarize_moderation_decisions(decisions: List[dict]) -> str:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(
        "gemini-pro"
    )  # Using gemini-pro as a concrete model identifier

    prompt = "Summarize the following moderation decisions and highlight any trends or critical issues:\n\n"
    for i, decision in enumerate(decisions):
        prompt += f"Decision {i + 1}:\n"
        prompt += f"  Text: {decision.get('text', 'N/A')}\n"
        prompt += f"  Is Safe: {decision.get('is_safe', 'N/A')}\n"
        prompt += f"  Reasons: {', '.join(decision.get('reasons', []))}\n"
        prompt += f"  Category Scores: {decision.get('category_scores', 'N/A')}\n\n"

    response = model.generate_content(prompt)
    return response.text
