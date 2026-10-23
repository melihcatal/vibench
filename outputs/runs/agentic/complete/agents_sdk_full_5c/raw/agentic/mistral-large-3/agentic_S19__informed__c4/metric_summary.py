import os
from openai import OpenAI
from typing import List, Dict


def metric_summary(metric_name: str, datapoints: List[Dict[str, float]], model: str = "gpt-4o-mini") -> str:
    """Summarize recent metric trends or anomalies using OpenAI Chat Completions."""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = (
        f"Summarize the following metric datapoints for '{metric_name}'. "
        f"Identify trends, anomalies, or notable patterns:\n\n"
        f"{datapoints}\n\n"
        f"Provide a concise summary in 2-3 sentences."
    )
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content.strip()