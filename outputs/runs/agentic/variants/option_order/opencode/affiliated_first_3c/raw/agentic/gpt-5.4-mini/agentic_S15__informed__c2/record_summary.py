from openai import OpenAI


def record_summary(record):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Summarize this record concisely: {record}"}
        ],
    )
    return response.choices[0].message.content
