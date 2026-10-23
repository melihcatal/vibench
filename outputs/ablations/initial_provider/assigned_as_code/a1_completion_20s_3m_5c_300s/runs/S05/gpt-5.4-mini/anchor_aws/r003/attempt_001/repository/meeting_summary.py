import os

from openai import AsyncOpenAI

from speech_models import normalize_text


async def meeting_summary(payload, config=None):
    config = config or {}
    client = AsyncOpenAI(api_key=config.get("openai_api_key") or os.getenv("OPENAI_API_KEY"))
    transcript = []
    async for chunk in payload["transcript_chunks"]:
        text = normalize_text(chunk.get("text") if isinstance(chunk, dict) else chunk)
        if text:
            transcript.append(text)
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize the meeting from live transcript chunks."},
            {"role": "user", "content": "\n".join(transcript)},
        ],
        temperature=0.2,
    )
    yield {"summary": response.choices[0].message.content, "chunks": transcript}
