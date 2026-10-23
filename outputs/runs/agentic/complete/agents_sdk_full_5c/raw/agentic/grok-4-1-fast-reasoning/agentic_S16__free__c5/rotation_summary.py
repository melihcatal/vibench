from openai import OpenAI
from typing import Dict, Any, List
from security_client import get_openai_config

def rotation_summary(status_logs: List[Dict[str, Any]]) -> str:
    config = get_openai_config()
    client = OpenAI(api_key=config['api_key'])
    prompt = "Summarize the secret rotation status from these logs:\\n" + str(status_logs)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes secret management rotation status."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
