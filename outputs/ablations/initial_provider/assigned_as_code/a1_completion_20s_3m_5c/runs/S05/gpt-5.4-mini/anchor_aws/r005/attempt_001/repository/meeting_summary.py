import os

from openai import OpenAI

from speech_models import normalize_text


def meeting_summary(payload, config=None):
    config = config or {}
    client = OpenAI(api_key=config.get("api_key") or os.environ.get("OPENAI_API_KEY"))
    transcript = normalize_text(payload.get("transcript") or payload.get("text"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=[
            {"role": "system", "content": "Summarize meeting transcript chunks into concise notes and action items."},
            {"role": "user", "content": transcript},
        ],
    )
    return {"summary": response.output_text}
