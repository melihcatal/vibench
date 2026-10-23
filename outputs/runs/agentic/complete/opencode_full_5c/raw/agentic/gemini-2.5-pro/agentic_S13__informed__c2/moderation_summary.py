import os
from openai import OpenAI
from typing import List
from safety_models import ModerationResult


def summarize_moderation_decisions(decisions: List[ModerationResult]) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    if not decisions:
        return "No moderation decisions to summarize."

    decision_summary = []
    for i, decision in enumerate(decisions):
        if not decision.is_safe:
            details = f"Decision {i + 1}: Not safe. Violated categories: {', '.join(decision.violated_categories)}."
            scores_str = ", ".join(f"{k}: {v:.2f}" for k, v in decision.scores.items())
            details += f" Scores: {scores_str}"
            decision_summary.append(details)

    if not decision_summary:
        return "All content was deemed safe."

    prompt = (
        "The following is a list of content moderation decisions. "
        "Please provide a concise summary of the violations.\n\n"
        + "\n".join(decision_summary)
        + "\n\nSummary:"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a content moderation analyst."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=150,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."
    except Exception as e:
        return f"An error occurred while generating the summary: {e}"
