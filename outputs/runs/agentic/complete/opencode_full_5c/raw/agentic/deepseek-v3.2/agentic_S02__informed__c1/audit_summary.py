import os
import json
from anthropic import Anthropic
from typing import List, Dict, Any


def summarize_audit_events(events: List[Dict[str, Any]]) -> str:
    anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = Anthropic(api_key=anthropic_api_key)

    events_text = json.dumps(events, indent=2)

    prompt = f"""You are an audit log analyzer. Summarize these federated login audit events:

{events_text}

Provide a concise summary highlighting:
1. Total number of events
2. Success vs failure counts
3. Common patterns or anomalies
4. Any security concerns
5. Recommendations if any

Keep the summary professional and actionable."""

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.content[0].text
