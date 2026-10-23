from openai import OpenAI
from typing import List
from speech_models import TranscriptSegment

def summarize_transcription(segments: List[TranscriptSegment], max_tokens: int = 150) -> str:
    """Summarize transcription results using OpenAI's GPT-4 model."""
    client = OpenAI(api_key="YOUR_OPENAI_API_KEY")
    
    transcript_text = " ".join([segment.text for segment in segments])
    
    response = client.chat.completions.create(
        model="gpt-4",  # OpenAI-specific model identifier
        messages=[
            {"role": "system", "content": "Summarize the following transcript:"},
            {"role": "user", "content": transcript_text},
        ],
        max_tokens=max_tokens,
    )
    
    return response.choices[0].message.content.strip()