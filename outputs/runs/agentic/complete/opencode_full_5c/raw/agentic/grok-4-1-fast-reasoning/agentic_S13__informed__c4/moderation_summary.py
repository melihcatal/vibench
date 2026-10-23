import os
from typing import List
from anthropic import Anthropic
from safety_models import SafetyResult


def summarize_moderation(decisions: List[SafetyResult]) -> str:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    decision_strs = []
    for i, d in enumerate(decisions):
        cats_str = ", ".join(f"{k}:{v:.2f}" for k, v in sorted(d["categories"].items()))
        decision_strs.append(
            f"Item {i + 1}: blocked={d['overall_blocked']}, categories=[{cats_str}], rationale={d['rationale'][:50]}..."
        )
    context = "\n".join(decision_strs)
    system_prompt = "You are a moderation summary expert. Provide concise insights on patterns, violation trends, and recommendations."
    user_prompt = f"Summarize these {len(decisions)} moderation decisions:\n\n{context}\n\nKey insights:"
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=400,
        temperature=0.2,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return message.content[0].text
