import os
import openai
from typing import List, Dict, Any


def metric_summary(
    metric_data: List[Dict[str, Any]], model: str = "gpt-4o-mini"
) -> str:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    prompt = "Summarize recent metric trends or detect anomalies:\\n" + str(metric_data)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are an expert in observability and metrics analysis.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=300,
        temperature=0.3,
    )
    return response.choices[0].message.content
