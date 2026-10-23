import os
from openai import OpenAI
from speech_models import MeetingSummary

def summarize_meeting_chunk(transcript_text: str) -> MeetingSummary | None:
    """
    Summarizes a chunk of a live meeting transcript using OpenAI's GPT models.
    """
    try:
        # It's recommended to use the OPENAI_API_KEY environment variable
        # The client automatically reads it.
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Using a specific, cost-effective model
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert meeting assistant. Your task is to provide a brief, concise summary of the provided meeting transcript chunk. Focus on key decisions, action items, and important topics mentioned.",
                },
                {
                    "role": "user",
                    "content": transcript_text,
                },
            ],
            temperature=0.5,
            max_tokens=150,
        )

        summary_text = response.choices[0].message.content
        if summary_text:
            return MeetingSummary(
                original_text=transcript_text,
                summary_text=summary_text.strip()
            )
        return None

    except Exception as e:
        print(f"An error occurred during summarization: {e}")
        return None
