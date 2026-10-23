import os
from openai import OpenAI

def summarize_transcription_results(transcript_text: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Using a common OpenAI model
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts."},
            {"role": "user", "content": f"Please summarize the following transcript:

{transcript_text}"}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content
