import openai
import os
from typing import List, Dict, Any

def incident_summary(error_logs: List[Dict[str, Any]]) -> str:
    """
    Summarizes error-log findings from Datadog query for incident review using OpenAI GPT.
    """
    log_texts = [log.get("message", "") for log in error_logs][:20]
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = (
        "Summarize the incident from these error logs. Identify patterns, affected services, and possible causes:\n\n"
        + "\\n".join(log_texts)
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a SRE expert analyzing logs for incident management."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400,
        temperature=0.2
    )
    return response.choices[0].message.content.strip()
