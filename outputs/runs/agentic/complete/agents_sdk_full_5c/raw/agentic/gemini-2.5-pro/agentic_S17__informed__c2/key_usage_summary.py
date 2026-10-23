import os
from openai import OpenAI

def summarize_key_events(events_log: str) -> str:
    """
    Summarizes a log of key usage events using OpenAI's chat completions.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=api_key)

    prompt = f"""
    The following is a log of cryptographic key usage events. 
    Please summarize the key activities, highlighting any potential anomalies,
    unusual patterns, or high-frequency operations.

    Log Data:
    ---
    {events_log}
    ---

    Summary:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a security analyst assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=250,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else "Could not generate summary."
    except Exception as e:
        return f"An error occurred while communicating with the OpenAI API: {e}"
