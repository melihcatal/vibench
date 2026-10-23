from openai import OpenAI


def main(log_finding: str) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Summarize incident findings for review."},
            {"role": "user", "content": log_finding},
        ],
    )
    return response.choices[0].message.content or ""
