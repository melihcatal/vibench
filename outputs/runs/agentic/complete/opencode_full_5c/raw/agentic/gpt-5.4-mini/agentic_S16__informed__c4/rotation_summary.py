from openai import OpenAI


def rotation_summary(notes):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Summarize secret rotation status."},
            {"role": "user", "content": notes},
        ],
    )
    return response.choices[0].message.content
