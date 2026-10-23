from openai import OpenAI

from speech_models import caption_chunks_to_text, CaptionChunk


def meeting_summary(chunks: list[CaptionChunk]):
    client = OpenAI()
    text = caption_chunks_to_text(chunks)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Summarize the meeting transcript."},
            {"role": "user", "content": text},
        ],
    )
    return response.choices[0].message.content
