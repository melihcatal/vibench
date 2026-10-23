import os

from openai import OpenAI


def summarize_incident(log_findings: str) -> str:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize error logs for incident review."},
            {"role": "user", "content": log_findings},
        ],
    )
    return response.choices[0].message.content or ""


def main() -> None:
    summarize_incident("error logs indicate repeated timeouts")


if __name__ == "__main__":
    main()
