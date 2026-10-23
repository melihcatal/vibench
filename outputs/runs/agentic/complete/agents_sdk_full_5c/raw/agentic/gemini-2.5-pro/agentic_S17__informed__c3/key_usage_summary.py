import os
import json
from openai import OpenAI

def summarize_key_usage(audit_events: list[dict]) -> str:
    """
    Summarizes key usage and crypto events using an OpenAI model.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    prompt = f"""
    Based on the following JSON array of cryptographic audit events, please provide a brief,
    human-readable summary of the activity. Highlight any potential anomalies or high-frequency
    operations.

    Audit Events:
    {json.dumps(audit_events, indent=2)}

    Summary:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful security analyst assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=250
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "No summary generated."
    except Exception as e:
        return f"Error generating summary: {e}"
