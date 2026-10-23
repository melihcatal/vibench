from typing import List
from safety_client import configure_google_genai
from safety_models import ModerationResult


def summarize_moderation_decisions(decisions: List[ModerationResult]) -> str:
    """
    Summarizes a list of moderation decisions using Google's Gemini Pro.
    """
    genai = configure_google_genai()
    model = genai.GenerativeModel("gemini-pro")

    flagged_count = sum(1 for d in decisions if d.results[0].flagged)

    prompt = f"""
    Here are {len(decisions)} moderation decisions.
    {flagged_count} of them were flagged as potentially unsafe.
    
    Summarize the key reasons for flagging based on the categories.
    For example: "The main issues were related to hate speech and violence."
    
    Decisions:
    """

    for decision in decisions:
        if decision.results[0].flagged:
            categories = [
                cat
                for cat, flagged in decision.results[0].categories.items()
                if flagged
            ]
            prompt += f"- Flagged for: {', '.join(categories)}\n"

    response = model.generate_content(prompt)
    return response.text
