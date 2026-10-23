from typing import Any, Dict

from openai import OpenAI


def metric_summary(metric_name: str, series: Dict[str, Any]) -> Dict[str, Any]:
    client = OpenAI()
    prompt = f"Summarize recent trends and anomalies for {metric_name} from this data: {series}"
    completion = client.chat.completions.create(
        model="gpt-5.4-mini", messages=[{"role": "user", "content": prompt}]
    )
    return {"summary": completion.choices[0].message.content}
