from openai import OpenAI


def summarize_meeting(transcript_chunks) -> str:
    client = OpenAI()
    text = "\n".join(transcript_chunks)
    response = client.responses.create(
        model="gpt-4.1-mini", input=f"Summarize this meeting transcript:\n{text}"
    )
    return response.output_text
