import os
from typing import List
from openai import OpenAI

from safety_models import ModerationDecision

def summarize_moderation_decisions(decisions: List[ModerationDecision]) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    decision_texts = []
    for decision in decisions:
        decision_texts.append(f"- Text: '{decision.text}' | Decision: {decision.decision} | Reason: {decision.reason}")

    prompt = f"""Summarize the following moderation decisions. Provide a concise overview of the overall content safety status and highlight any recurring patterns or critical issues.\n\nModeration Decisions:\n{'\n'.join(decision_texts)}\n\nSummary:"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes moderation decisions."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )

    return response.choices[0].message.content