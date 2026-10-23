from openai import OpenAI
import os


def summarize_error_logs(log_entries: list) -> str:
    """Summarize error-log findings for incident review using OpenAI."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    log_texts = "\n".join([
        f"Timestamp: {log.get('timestamp')}, Message: {log.get('message')}, Attributes: {log.get('attributes')}"
        for log in log_entries
    ])
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
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