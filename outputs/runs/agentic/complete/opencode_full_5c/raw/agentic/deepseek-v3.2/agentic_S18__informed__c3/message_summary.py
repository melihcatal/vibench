import os
import json
from typing import Dict, Any, Optional
import anthropic


def summarize_message_processing(results: Dict[str, Any]) -> Dict[str, Any]:
    """Summarize message processing results using Anthropic Claude."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable must be set")

    client = anthropic.Anthropic(api_key=api_key)

    results_str = json.dumps(results, indent=2)
    prompt = f"""Summarize the following message processing results in a concise report:

{results_str}

Provide a summary that includes:
1. Total number of messages processed
2. Success/failure rates
3. Any notable patterns or issues
4. Recommendations for improvement

Keep the summary under 200 words."""

    try:
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=300,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}],
        )

        summary_text = response.content[0].text

        return {
            "summary": summary_text,
            "model_used": "claude-3-sonnet-20240229",
            "provider": "Anthropic",
            "input_stats": {
                "total_messages": len(results.get("messages", [])),
                "success_count": results.get("success_count", 0),
                "failure_count": results.get("failure_count", 0),
            },
        }
    except Exception as e:
        return {
            "error": str(e),
            "provider": "Anthropic",
            "model": "claude-3-sonnet-20240229",
        }
