import os
from typing import List, Dict, Any
import json


def moderation_summary(decisions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Summarize moderation decisions using Anthropic Claude for analysis.
    """
    import anthropic

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = anthropic.Anthropic(api_key=api_key)

    # Prepare data for summary
    blocked_count = sum(1 for d in decisions if d.get("decision") == "block")
    allowed_count = len(decisions) - blocked_count

    blocked_samples = []
    for d in decisions:
        if d.get("decision") == "block" and len(blocked_samples) < 3:
            blocked_samples.append(
                {
                    "text": d.get("message", d.get("text", ""))[:100],
                    "severity": d.get("severity", 0),
                    "categories": list(d.get("categories", {}).keys())[:3],
                }
            )

    prompt = f"""You are a content moderation analyst. Summarize the following moderation batch results:

Total messages: {len(decisions)}
Blocked messages: {blocked_count}
Allowed messages: {allowed_count}

Blocked message samples (first 100 chars):
{json.dumps(blocked_samples, indent=2)}

Please provide a concise summary including:
1. Overall safety rate
2. Most common violation categories
3. Severity distribution
4. Any patterns or recommendations

Keep the summary professional and actionable for moderation teams."""

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )

        summary_text = response.content[0].text

        # Extract key metrics
        metrics = {
            "total_messages": len(decisions),
            "blocked_count": blocked_count,
            "allowed_count": allowed_count,
            "block_rate": blocked_count / len(decisions) if decisions else 0,
            "summary": summary_text,
            "provider": "anthropic",
            "model": "claude-3-5-sonnet-20241022",
        }

        return metrics

    except Exception as e:
        return {
            "error": str(e),
            "total_messages": len(decisions),
            "blocked_count": blocked_count,
            "allowed_count": allowed_count,
            "summary": "Failed to generate summary",
        }
