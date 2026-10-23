from typing import List
from safety_client import get_openai_client
from safety_models import ModerationDecision, ModerationSummary


def summarize_moderation_decisions(
    decisions: List[ModerationDecision],
) -> ModerationSummary:
    client = get_openai_client()

    if not decisions:
        return ModerationSummary(summary_text="No decisions to summarize.")

    prompt_content = "Summarize the following moderation decisions:\n\n"
    for d in decisions:
        prompt_content += f"- Text: '{d.text[:50]}...' Flagged: {d.flagged}. Scores: {d.scores.dict(exclude_none=True)}\n"

    prompt_content += "\nProvide a brief, high-level summary of these actions."

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a moderation analyst's assistant."},
            {"role": "user", "content": prompt_content},
        ],
        max_tokens=150,
        temperature=0.5,
    )

    summary = (
        response.choices[0].message.content
        if response.choices
        else "Could not generate summary."
    )

    return ModerationSummary(summary_text=summary)
