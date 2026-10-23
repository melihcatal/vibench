import os
from typing import List
from openai import OpenAI

async def summarize_meeting_chunks(transcript_chunks: List[str]) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set.")

    # Provider-specific: OpenAI Chat Completions API
    client = OpenAI(api_key=api_key)

    full_transcript = " ".join(transcript_chunks)

    prompt = f"Summarize the following meeting transcript:

{full_transcript}

Summary:"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo", # Provider-specific model identifier
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200
    )
    summary = response.choices[0].message.content.strip()
    return summary
