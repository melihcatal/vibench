import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
_openai_client = OpenAI(api_key=OPENAI_API_KEY)


def summarize_transcript_chunk(chunk: str) -> str:
    if not chunk.strip():
        return ""
    response = _openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize the following meeting transcript chunk concisely."},
            {"role": "user", "content": chunk}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()