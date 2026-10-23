from openai import OpenAI

from speech_models import normalize_segments


def archive_summary(payload: dict) -> str:
    client = OpenAI()
    segments = normalize_segments(payload)
    text = "\n".join(
        segment.get("text", "") for segment in segments if segment.get("text")
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Summarize this meeting transcript for archive:\n{text}",
            }
        ],
    )
    return response.choices[0].message.content
