import os
from openai import OpenAI
from typing import List

def summarize_meeting_transcript(transcript_chunks: List[str]) -> str:
    """
    Summarizes a list of live meeting transcript chunks using OpenAI.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "Error: OPENAI_API_KEY is not set."

    client = OpenAI(api_key=api_key)
    full_transcript = "\n".join(transcript_chunks)

    if not full_transcript.strip():
        return "The transcript is empty, nothing to summarize."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes meeting transcripts. Provide a concise summary of the key points and action items.",
                },
                {
                    "role": "user",
                    "content": f"Please summarize the following transcript:\n\n{full_transcript}",
                },
            ],
            temperature=0.5,
        )
        summary = response.choices[0].message.content
        return summary if summary else "Failed to generate summary."
    except Exception as e:
        return f"An error occurred while summarizing: {e}"
