import os
from openai import OpenAI

def summarize_live_meeting(transcript_chunks: list[str]) -> str:
    """
    Summarizes a list of live meeting transcript chunks using OpenAI.

    Args:
        transcript_chunks: A list of strings, where each string is a
                           chunk of the meeting transcript.

    Returns:
        A string containing the summary of the meeting.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    full_transcript = "\n".join(transcript_chunks)

    if not full_transcript.strip():
        return "The transcript is empty, no summary can be generated."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant specialized in summarizing meetings. "
                               "Provide a concise summary of the following transcript, "
                               "highlighting key decisions and action items."
                },
                {
                    "role": "user",
                    "content": full_transcript,
                }
            ],
            temperature=0.5,
        )
        summary = response.choices[0].message.content
        return summary if summary else "Failed to generate summary."
    except Exception as e:
        return f"An error occurred while communicating with the OpenAI API: {e}"
