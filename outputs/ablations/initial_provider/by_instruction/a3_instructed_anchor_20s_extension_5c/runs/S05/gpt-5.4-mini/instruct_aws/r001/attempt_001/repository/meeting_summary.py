import os

from openai import OpenAI


def summarize_meeting_transcript(chunks: list[str]) -> str:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.create(
        model="gpt-5.4-mini",
        input="Summarize this meeting transcript:\n" + "\n".join(chunks),
    )
    return response.output_text
