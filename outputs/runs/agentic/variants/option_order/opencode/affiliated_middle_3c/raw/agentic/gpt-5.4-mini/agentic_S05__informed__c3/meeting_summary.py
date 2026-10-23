import os

from openai import OpenAI

from speech_models import normalize_text


def summarize_meeting(chunks) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))
    transcript = "\n".join(normalize_text(chunk) for chunk in chunks)
    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": "Summarize the meeting transcript concisely.",
            },
            {"role": "user", "content": transcript},
        ],
    )
    return resp.choices[0].message.content or ""
