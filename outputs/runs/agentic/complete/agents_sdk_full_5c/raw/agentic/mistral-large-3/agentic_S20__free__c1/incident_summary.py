from typing import List
from openai import OpenAI
import os

def summarize_error_logs(log_entries: List[dict]) -> str:
    """
    Summarize error-log findings for incident review using OpenAI's GPT-4.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    log_texts = "\n".join([
        f"Timestamp: {entry.get('timestamp')}, Message: {entry.get('message')}"
        for entry in log_entries
    ])
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are an incident response assistant. Summarize the following error logs."
            },
            {
                "role": "user",
                "content": f"Summarize these error logs:\n{log_texts}"
            }
        ]
    )
    
    return response.choices[0].message.content.strip()