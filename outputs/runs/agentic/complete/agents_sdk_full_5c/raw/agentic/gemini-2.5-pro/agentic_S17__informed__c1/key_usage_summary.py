# key_usage_summary.py
import os
from openai import OpenAI
from typing import List
from security_models import AuditLog

def summarize_key_usage(logs: List[AuditLog]) -> str:
    """
    Summarizes key usage audit logs using OpenAI's GPT model.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    client = OpenAI(api_key=api_key)

    prompt_content = "Summarize the following crypto key audit logs into a brief, human-readable report. Highlight any unusual activity:\n\n"
    for log in logs:
        prompt_content += f"- Timestamp: {log.timestamp}, User: {log.user}, Event: {log.event_name}, Details: {log.details}\n"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a security analyst assistant."},
                {"role": "user", "content": prompt_content}
            ],
            temperature=0.5,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"An error occurred while summarizing with OpenAI: {e}")
        return "Failed to generate summary."
