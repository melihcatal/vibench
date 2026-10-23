from openai import OpenAI


def rotation_summary(notes: str) -> str:
    client = OpenAI()
    resp = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "user", "content": f"Summarize secret rotation status: {notes}"}
        ],
    )
    return resp.choices[0].message.content
