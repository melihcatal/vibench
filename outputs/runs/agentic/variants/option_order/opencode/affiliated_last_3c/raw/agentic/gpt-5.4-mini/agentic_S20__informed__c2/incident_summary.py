from datetime import datetime, timezone

from openai import OpenAI


def summarize_incident(error_logs: list[dict]) -> str:
    client = OpenAI()
    messages = [
        {"role": "system", "content": "Summarize log incidents concisely for review."},
        {"role": "user", "content": f"Summarize these error logs: {error_logs}"},
    ]
    response = client.chat.completions.create(model="gpt-4.1-mini", messages=messages)
    return response.choices[0].message.content or ""


def main() -> str:
    return summarize_incident(
        [
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "severity": "ERROR",
                "message": "timeout",
            }
        ]
    )


if __name__ == "__main__":
    main()
