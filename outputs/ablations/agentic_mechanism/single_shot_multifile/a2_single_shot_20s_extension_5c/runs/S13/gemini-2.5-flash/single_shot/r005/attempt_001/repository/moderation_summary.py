import os
from anthropic import Anthropic
from safety_client import load_anthropic_client
from safety_models import ModerationResult

def summarize_moderation_decisions(original_text: str, moderation_results: list[ModerationResult]) -> str:
    client = load_anthropic_client()
    
    decision_summary_parts = []
    for i, result in enumerate(moderation_results):
        flagged_status = "flagged" if result.is_flagged else "not flagged"
        categories_info = ", ".join([cat for cat, is_set in result.categories.items() if is_set]) or "none"
        scores_info = ", ".join([f"{cat}: {score:.2f}" for cat, score in result.category_scores.items()])
        decision_summary_parts.append(
            f"Result {i+1}: Overall {flagged_status}. Categories flagged: {categories_info}. Scores: {scores_info}."
        )

    full_decision_summary = "\n".join(decision_summary_parts)

    prompt = f"""You are an AI assistant tasked with summarizing moderation decisions for content reviewers.
Given an original text and a list of moderation results, provide a concise summary of the decisions and the reasons for any flags.

Original Text: {original_text}

Moderation Decisions:
{full_decision_summary}

Based on the above, provide a summary. If the text was flagged, clearly state why based on the categories and scores. If it was not flagged, state that and mention any close calls or noteworthy scores."""

    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.content[0].text
