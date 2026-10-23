import os
from openai import OpenAI


def summarize_meeting_chunk(transcript_chunk: str):
    """
    Summarize live meeting transcript chunks using OpenAI's GPT models.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in environment variables.")

    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes meeting transcripts.",
                },
                {
                    "role": "user",
                    "content": f"Please summarize the following part of a meeting transcript:\n\n{transcript_chunk}",
                },
            ],
            max_tokens=150,
        )
        summary = response.choices[0].message.content
        return summary.strip()
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None
