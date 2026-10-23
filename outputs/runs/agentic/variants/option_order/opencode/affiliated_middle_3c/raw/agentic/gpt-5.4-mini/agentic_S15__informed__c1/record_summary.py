from openai import OpenAI


def record_summary(record: dict) -> str:
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": f"Summarize this record in one sentence: {record}",
            }
        ],
    )
    return response.choices[0].message.content or ""
