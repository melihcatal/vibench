from typing import List
import json

from safety_client import get_anthropic_client
from safety_models import SafetyDecision, ModerationSummary


def summarize_moderation_decisions(decisions: List[SafetyDecision]) -> ModerationSummary:
    """
    Summarizes a list of moderation decisions using Anthropic's Claude model.
    """
    client = get_anthropic_client()
    if not client:
        return ModerationSummary(
            overall_decision="Error",
            summary_text="Anthropic client not configured.",
            key_themes=[],
            confidence=0.0
        )

    decisions_str = "\n".join(
        [f"- Text: '{d.text}', Safe: {d.is_safe}, Reason: {d.reason}" for d in decisions]
    )

    prompt = f"""
    Here are a series of content moderation decisions:
    {decisions_str}

    Please provide a summary of these decisions. I need a JSON object with the following fields:
    - "overall_decision": A single word, either "ACCEPT", "REJECT", or "REVIEW".
    - "summary_text": A one-sentence summary of the reasons for the decisions.
    - "key_themes": A list of strings identifying the main policy violation themes found (e.g., "Hate Speech", "Spam").
    - "confidence": A float from 0.0 to 1.0 indicating your confidence in the summary.

    Provide only the JSON object.
    """

    try:
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=512,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        response_text = message.content[0].text
        response_json = json.loads(response_text)
        
        return ModerationSummary(**response_json)

    except Exception as e:
        return ModerationSummary(
            overall_decision="Error",
            summary_text=f"API Error: {e}",
            key_themes=[],
            confidence=0.0
        )
