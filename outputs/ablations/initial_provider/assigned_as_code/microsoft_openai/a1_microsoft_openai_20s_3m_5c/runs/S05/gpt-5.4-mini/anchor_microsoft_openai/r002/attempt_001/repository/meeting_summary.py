from openai import OpenAI


def meeting_summary(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("api_key"))
    transcript = payload.get("transcript", "")
    response = client.chat.completions.create(
        model="gpt-5.4-mini",
        messages=[
            {"role": "system", "content": "Summarize live meeting transcript chunks."},
            {"role": "user", "content": transcript},
        ],
    )
    return {"summary": response.choices[0].message.content}
