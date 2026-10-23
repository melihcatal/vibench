from openai import OpenAI


def summarize_meeting_transcript(chunks: list[str]) -> str:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input="Summarize this live meeting transcript: " + " ".join(chunks),
    )
    return response.output_text
