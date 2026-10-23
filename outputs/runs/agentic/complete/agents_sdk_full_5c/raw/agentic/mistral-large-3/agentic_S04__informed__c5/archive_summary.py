import os
from typing import List, Dict
from openai import OpenAI

def summarize_transcription(segments: List[Dict[str, str]]) -> str:
    """
    Summarizes transcription results using OpenAI's GPT-4 model.
    Returns a concise summary of the transcript.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    
    client = OpenAI(api_key=api_key)
    
    transcript_text = " ".join([segment["text"] for segment in segments])
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes meeting transcripts."},
            {"role": "user", "content": f"Summarize the following transcript:\n\n{transcript_text}"}
        ],
        max_tokens=500
    )
    
    return response.choices[0].message.content.strip()