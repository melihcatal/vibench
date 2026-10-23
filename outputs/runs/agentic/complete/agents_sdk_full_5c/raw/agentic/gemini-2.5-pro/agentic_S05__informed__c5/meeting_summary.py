from openai import OpenAI
from dotenv import load_dotenv

from speech_models import MeetingSummary

load_dotenv()

def summarize_meeting_chunk(transcript_chunk: str) -> MeetingSummary | None:
    """
    Summarizes a chunk of a meeting transcript using OpenAI's GPT model.

    Args:
        transcript_chunk: A string containing a portion of the meeting transcript.

    Returns:
        A MeetingSummary object or None if an error occurs.
    """
    try:
        # The OpenAI client automatically reads the OPENAI_API_KEY from env vars.
        client = OpenAI()
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at summarizing meeting transcripts. "
                               "Provide a concise summary of the following transcript chunk."
                },
                {
                    "role": "user",
                    "content": transcript_chunk,
                },
            ],
            temperature=0.5,
            max_tokens=150,
        )
        
        summary_text = response.choices[0].message.content
        if summary_text:
            return MeetingSummary(summary_text=summary_text.strip())
        return None

    except Exception as e:
        print(f"An error occurred while summarizing: {e}")
        return None
