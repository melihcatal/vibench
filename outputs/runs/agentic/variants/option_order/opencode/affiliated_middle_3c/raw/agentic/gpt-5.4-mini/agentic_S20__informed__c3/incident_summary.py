from openai import OpenAI


def main(log_findings: str) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize log findings for incident review.",
            },
            {"role": "user", "content": log_findings},
        ],
    )
    return response.choices[0].message.content or ""
