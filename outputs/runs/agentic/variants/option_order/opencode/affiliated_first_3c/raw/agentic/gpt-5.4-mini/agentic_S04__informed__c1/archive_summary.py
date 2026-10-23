from openai import OpenAI


def archive_summary(transcript: str) -> str:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini", input=f"Summarize for archive: {transcript}"
    )
    return response.output_text
