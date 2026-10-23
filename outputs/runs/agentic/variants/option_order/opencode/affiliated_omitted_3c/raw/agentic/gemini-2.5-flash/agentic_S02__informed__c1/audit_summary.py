import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def summarize_audit_events(audit_events: str) -> str:
    if not OPENAI_API_KEY:
        raise ValueError("Missing OPENAI_API_KEY environment variable")

    client = OpenAI(api_key=OPENAI_API_KEY)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that summarizes security audit events."},
                {"role": "user", "content": f"Summarize the following federated login audit events:

{audit_events}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error summarizing audit events: {e}"
