import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_live_meeting(transcript_chunks):
    """Summarize live meeting transcript chunks using OpenAI GPT."""
    full_transcript = ""
    for chunk in transcript_chunks:
        full_transcript += chunk + " "
        if len(full_transcript.split()) > 100:  # Summarize every ~100 words
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful meeting summarizer."},
                    {"role": "user", "content": f"Summarize the meeting discussion so far: {full_transcript}"}
                ],
                max_tokens=150
            )
            summary = response.choices[0].message.content
            full_transcript = ""  # Reset for next
            yield summary
    if full_transcript:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful meeting summarizer."},
                {"role": "user", "content": f"Summarize the meeting discussion: {full_transcript}"}
            ],
            max_tokens=150
        )
        yield response.choices[0].message.content
