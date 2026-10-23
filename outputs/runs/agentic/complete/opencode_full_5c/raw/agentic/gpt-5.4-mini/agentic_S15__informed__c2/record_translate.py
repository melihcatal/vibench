from openai import OpenAI


def record_translate(record, target_language="en"):
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": f"Translate user-facing fields to {target_language}."},
            {"role": "user", "content": str(record)},
        ],
    )
    return response.choices[0].message.content
