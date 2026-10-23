from openai import OpenAI


def record_summary(record):
    client = OpenAI()
    text = str(record)
    completion = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "user", "content": f"Summarize this record briefly: {text}"}
        ],
    )
    return completion.choices[0].message.content
