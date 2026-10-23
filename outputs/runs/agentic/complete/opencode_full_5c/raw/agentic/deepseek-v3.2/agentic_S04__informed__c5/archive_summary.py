import os
import openai
from typing import Dict


def archive_summary(transcript_text: str, max_length: int = 500) -> Dict[str, str]:
    """Summarize transcription results using OpenAI GPT."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = openai.OpenAI(api_key=api_key)

    prompt = f"""Please provide a concise summary of the following transcript. 
    Focus on key points, decisions made, action items, and important discussions.
    
    Transcript:
    {transcript_text[:4000]}
    
    Summary:"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes meeting transcripts.",
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=max_length,
        temperature=0.3,
    )

    summary = response.choices[0].message.content.strip()

    return {
        "summary": summary,
        "model": "gpt-3.5-turbo",
        "transcript_length": len(transcript_text),
        "summary_length": len(summary),
    }
