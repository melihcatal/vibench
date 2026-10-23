import os
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")


def summarize_audit_events(audit_events: str) -> str:
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY must be set in environment variables.")

    client = OpenAI(api_key=OPENAI_API_KEY)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Using a concrete model identifier
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes security audit events.",
                },
                {
                    "role": "user",
                    "content": f"Summarize the following federated login audit events:\n\n{audit_events}",
                },
            ],
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        return f"Error summarizing audit events: {e}"
