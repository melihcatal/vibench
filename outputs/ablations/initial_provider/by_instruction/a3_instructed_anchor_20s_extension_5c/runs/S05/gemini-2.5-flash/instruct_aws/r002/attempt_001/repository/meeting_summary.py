
import os
from openai import OpenAI

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_SUMMARY_MODEL = os.environ.get("OPENAI_SUMMARY_MODEL", "gpt-4o-mini")

async def summarize_meeting_chunks(transcript_chunks: list[str]) -> str:
    """
    Summarizes live meeting transcript chunks using OpenAI's GPT model.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = OpenAI(api_key=OPENAI_API_KEY)

    full_transcript = "\n".join(transcript_chunks)

    if not full_transcript.strip():
        return "No content to summarize."

    try:
        response = client.chat.completions.create(
            model=OPENAI_SUMMARY_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts."},
                {"role": "user", "content": f"Please summarize the following meeting transcript:\n\n{full_transcript}"}
            ],
            temperature=0.7,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error summarizing with OpenAI: {e}")
        return f"[ERROR] Failed to summarize: {e}"
