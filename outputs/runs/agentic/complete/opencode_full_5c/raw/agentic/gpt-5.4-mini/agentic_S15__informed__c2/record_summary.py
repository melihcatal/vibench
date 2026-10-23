from openai import OpenAI


def record_summary(record):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "Summarize the document record concisely."},
            {"role": "user", "content": str(record)},
        ],
    )
    return response.choices[0].message.content
