import os
from typing import List, Dict
from openai import OpenAI


def moderation_summary(moderation_decisions: List[Dict]) -> str:
    """Summarize moderation decisions."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    blocked_count = sum(1 for d in moderation_decisions if d.get("decision") == "block")
    allowed_count = sum(1 for d in moderation_decisions if d.get("decision") == "allow")
    error_count = sum(1 for d in moderation_decisions if d.get("decision") == "error")

    blocked_examples = [
        f"Message: {d.get('message', '')[:50]}... - Categories: {', '.join(d.get('categories_flagged', []))}"
        for d in moderation_decisions
        if d.get("decision") == "block"
    ][:3]

    prompt = f"""You are a moderation system analyst. Summarize the following moderation results:

Total decisions: {len(moderation_decisions)}
- Blocked: {blocked_count}
- Allowed: {allowed_count}
- Errors: {error_count}

Examples of blocked content:
{chr(10).join(blocked_examples) if blocked_examples else "No blocked content"}

Provide a concise summary highlighting:
1. Overall safety level
2. Most common violation categories
3. Any patterns or trends
4. Recommendations for policy adjustments if needed

Summary:"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful moderation analyst."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
            temperature=0.3,
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating summary: {str(e)}"
