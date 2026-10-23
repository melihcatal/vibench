from openai import OpenAI


def meeting_summary(chunks):
    client = OpenAI()
    transcript = "\n".join(chunks)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize live meeting transcript chunks."},
            {"role": "user", "content": transcript},
        ],
    )
    return response.choices[0].message.content
