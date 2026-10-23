import os
from openai import OpenAI

def summarize_transcript_chunk(chunk_text):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes meeting transcripts.",
            },
            {"role": "user", "content": f"Summarize this meeting transcript:\n\n{chunk_text}"},
        ],
        max_tokens=150,
    )

    return response.choices[0].message.content.strip()