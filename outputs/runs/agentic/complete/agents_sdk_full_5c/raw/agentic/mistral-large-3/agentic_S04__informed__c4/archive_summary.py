from typing import List
from anthropic import Anthropic
from speech_models import SpeakerLabel


def archive_summary(segments: List[SpeakerLabel], max_tokens: int = 1000) -> str:
    """
    Summarize transcription results using Anthropic's Claude model.
    Returns a concise summary of the transcript.
    """
    client = Anthropic()
    transcript_text = " \n".join([f"Speaker {segment.speaker}: {segment.text}" for segment in segments])
    
    response = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=max_tokens,
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following transcript:\n\n{transcript_text}"
            }
        ]
    )
    
    return response.content[0].text