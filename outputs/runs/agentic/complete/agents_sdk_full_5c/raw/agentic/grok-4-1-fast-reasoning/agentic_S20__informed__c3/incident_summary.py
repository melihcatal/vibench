import openai
import os
from typing import List, Dict, Any

def incident_summary(log_entries: List[Dict[str, Any]]) -> str:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    logs_text = "\n".join([f"{entry.get('timestamp', 'N/A')}: {entry.get('message', '')}" for entry in log_entries])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert incident response analyst. Provide a concise summary of the incident, key errors, and potential root causes."},
            {"role": "user", "content": f"Summarize this incident from logs:\n{logs_text}"}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content