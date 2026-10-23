from openai import OpenAI


def archive_summary(transcript_text: str) -> str:
    client = OpenAI()
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=f"Summarize this transcription for archiving:\n\n{transcript_text}",
    )
    return response.output_text
