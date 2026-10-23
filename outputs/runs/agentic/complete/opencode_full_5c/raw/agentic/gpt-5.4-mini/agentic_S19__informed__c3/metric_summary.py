from datetime import datetime, timedelta

from openai import OpenAI


def metric_summary(metric_name, recent_points):
    client = OpenAI()
    prompt = f"Summarize recent trend and anomalies for {metric_name} from points: {recent_points}"
    response = client.chat.completions.create(
        model="gpt-5.4-mini", messages=[{"role": "user", "content": prompt}]
    )
    return {
        "metric_name": metric_name,
        "summary": response.choices[0].message.content,
        "generated_at": datetime.utcnow().isoformat(),
    }
