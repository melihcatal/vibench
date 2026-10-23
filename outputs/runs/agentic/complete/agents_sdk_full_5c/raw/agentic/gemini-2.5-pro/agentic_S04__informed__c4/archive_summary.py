import os
from openai import OpenAI

def summarize_transcript(full_transcript_text: str) -> str:
    """
    Summarizes the full text of a transcript using OpenAI's GPT models.

    Args:
        full_transcript_text: A string containing the entire transcript.

    Returns:
        A string containing the summary.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    if not full_transcript_text:
        return ""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes meeting transcripts. "
                           "Provide a concise summary of the key points and action items."
            },
            {
                "role": "user",
                "content": f"Please summarize the following transcript:\n\n{full_transcript_text}"
            }
        ],
        temperature=0.5,
        max_tokens=256
    )
    
    return response.choices[0].message.content.strip()
