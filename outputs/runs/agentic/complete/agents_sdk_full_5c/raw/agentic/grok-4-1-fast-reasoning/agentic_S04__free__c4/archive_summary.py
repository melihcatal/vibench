import os
import openai

def archive_summary(transcript: str) -> str:
    """
    Summarize transcription results.
    """
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes transcripts concisely."},
            {"role": "user", "content": transcript}
        ],
        max_tokens=500,
    )
    return response.choices[0].message.content