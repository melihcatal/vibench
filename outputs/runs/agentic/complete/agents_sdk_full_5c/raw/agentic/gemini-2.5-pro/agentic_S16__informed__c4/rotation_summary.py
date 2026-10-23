import os
from openai import OpenAI
from typing import List, Dict, Any

def summarize_rotation_events(events: List[Dict[str, Any]]) -> str:
    """
    Summarizes a list of secret rotation events using OpenAI's GPT model.

    Args:
        events: A list of dictionaries, each representing a rotation event.

    Returns:
        A concise summary of the rotation events.
    """
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    prompt_text = "Summarize the following secret rotation events. Note any failures or unusual activity:\n\n"
    for event in events:
        prompt_text += f"- Secret: {event['secret_name']}, Status: {event['status']}, Timestamp: {event['timestamp']}\n"

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a security analyst assistant."},
                {"role": "user", "content": prompt_text},
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "Could not generate summary."
