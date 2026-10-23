import os
from typing import List, Dict, Any
from anthropic import Anthropic


def message_summary(
    messages: List[Dict[str, Any]], summary_type: str = "brief"
) -> Dict[str, Any]:
    """Summarize message processing results using Anthropic Claude."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    client = Anthropic(api_key=api_key)

    # Prepare messages for summarization
    message_texts = []
    for i, msg in enumerate(messages):
        if isinstance(msg, dict):
            msg_str = str(msg)
        else:
            msg_str = str(msg)
        message_texts.append(f"Message {i + 1}: {msg_str[:500]}...")

    prompt = f"""Please provide a {summary_type} summary of these {len(messages)} messages:

{" ".join(message_texts)}

Summary should include:
1. Main themes or topics
2. Any patterns or trends
3. Key statistics (if applicable)
4. Notable issues or successes

Provide the summary in a structured format."""

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )

        summary_text = response.content[0].text

        return {
            "summary": summary_text,
            "message_count": len(messages),
            "summary_type": summary_type,
            "model_used": "claude-3-haiku-20240307",
            "provider": "Anthropic",
        }
    except Exception as e:
        return {
            "error": str(e),
            "message_count": len(messages),
            "summary": "Failed to generate summary",
            "provider": "Anthropic",
        }
