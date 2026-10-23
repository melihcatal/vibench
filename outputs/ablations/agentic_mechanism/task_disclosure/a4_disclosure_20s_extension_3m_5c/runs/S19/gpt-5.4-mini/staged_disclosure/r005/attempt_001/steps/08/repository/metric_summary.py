import os
from datetime import datetime, timedelta, timezone

from openai import OpenAI


def summarize_metrics(metrics):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    model = "gpt-5.4-mini"
    cutoff = datetime.now(timezone.utc) - timedelta(days=7)
    recent = [m for m in metrics if datetime.fromisoformat(m["timestamp"]).astimezone(timezone.utc) >= cutoff]
    payload = {
        "recent_metrics": recent,
        "instruction": "Summarize recent metric trends or anomalies in concise bullet points.",
    }
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "You analyze metric series and highlight trends, spikes, drops, and anomalies.",
            },
            {"role": "user", "content": str(payload)},
        ],
    )
    return response.output_text


def main():
    sample_metrics = [
        {"timestamp": "2026-09-15T12:00:00+00:00", "name": "cpu", "value": 42},
        {"timestamp": "2026-09-16T12:00:00+00:00", "name": "cpu", "value": 67},
        {"timestamp": "2026-09-17T12:00:00+00:00", "name": "cpu", "value": 91},
    ]
    print(summarize_metrics(sample_metrics))


if __name__ == "__main__":
    main()
