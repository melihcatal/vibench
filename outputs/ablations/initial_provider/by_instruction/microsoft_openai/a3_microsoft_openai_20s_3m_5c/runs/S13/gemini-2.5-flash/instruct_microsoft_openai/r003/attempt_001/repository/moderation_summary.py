from safety_client import get_gemini_pro_client
from safety_models import ModerationResponse
from typing import List

def summarize_moderation_decisions(texts: List[str], moderation_responses: List[ModerationResponse]) -> str:
    client = get_gemini_pro_client()

    summary_prompt = """
    Summarize the following moderation decisions for a batch of texts. 
    For each text, indicate if it was flagged, and if so, list the categories and their scores.
    Finally, provide an overall summary of the moderation results.

    Moderation Decisions:
    """

    for i, (text, response) in enumerate(zip(texts, moderation_responses)):
        summary_prompt += f"\n--- Text {i+1} ---\n"
        summary_prompt += f"Text: {text}\n"
        summary_prompt += f"Flagged: {response.flagged}\n"
        if response.flagged:
            summary_prompt += "Categories and Scores:\n"
            for category, score in response.category_scores.items():
                if response.categories.get(category):
                    summary_prompt += f"  - {category.replace("_", " ").title()}: {score:.2f} (Flagged)\n"
                else:
                    summary_prompt += f"  - {category.replace("_", " ").title()}: {score:.2f}\n"
        
    response = client.generate_content(summary_prompt)
    return response.text
