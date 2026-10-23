import json
import os

import openai

from safety_models import BatchModerationResponse, SafetyResponse

MODEL_ID = "gpt-4o"


def _build_moderation_context(
    decisions: BatchModerationResponse | list[SafetyResponse],
) -> str:
    if isinstance(decisions, BatchModerationResponse):
        results = decisions.results
    else:
        results = decisions

    lines = []
    for i, result in enumerate(results, 1):
        status = "SAFE" if result.is_safe else "FLAGGED"
        lines.append(f"Message {i}: [{status}]")
        for cat_score in result.category_scores:
            lines.append(
                f"  - {cat_score.category}: {cat_score.score:.2f} ({cat_score.severity})"
            )
        if result.flagged_categories:
            lines.append(f"  Flagged: {', '.join(result.flagged_categories)}")
        lines.append("")
    return "\n".join(lines)


def summarize_moderation(
    decisions: BatchModerationResponse | list[SafetyResponse],
) -> str:
    context = _build_moderation_context(decisions)

    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    system_prompt = (
        "You are a content moderation analyst. Summarize the moderation decisions "
        "provided, highlighting key patterns, the most concerning categories, "
        "and an overall safety assessment. Be concise and structured."
    )

    user_prompt = (
        f"Here are the moderation results from Azure AI Content Safety:\n\n{context}\n\n"
        "Provide a structured summary with: 1) Overall safety assessment, "
        "2) Key risk patterns, 3) Recommendations."
    )

    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=500,
    )

    return response.choices[0].message.content.strip()
