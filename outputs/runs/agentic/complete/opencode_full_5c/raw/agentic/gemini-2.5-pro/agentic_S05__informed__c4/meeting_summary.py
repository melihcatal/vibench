import os
from openai import AsyncOpenAI
from typing import List


async def summarize_meeting_transcript(transcript_chunks: List[str]) -> str:
    """Summarizes live meeting transcript chunks using OpenAI."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    client = AsyncOpenAI(api_key=api_key)

    full_transcript = "\\n".join(transcript_chunks)

    prompt = f"""
    Please summarize the following meeting transcript.
    Provide a concise summary of the key discussion points, decisions, and action items.

    Transcript:
    {full_transcript}

    Summary:
    """

    try:
        response = await client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes meeting transcripts.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
        )
        summary = response.choices[0].message.content
        return summary.strip() if summary else ""
    except Exception as e:
        print(f"Error during summarization: {e}")
        return ""
