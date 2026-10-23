import os
from typing import List, Dict, Any
from anthropic import Anthropic
from speech_models import DiarizedUtterance


def archive_summary(utterances: List[DiarizedUtterance]) -> str:
    """
    Summarizes transcription results using Anthropic's Claude model.
    """
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    transcript_text = " \n".join(
        [f"Speaker {utterance.speaker}: {utterance.text}" for utterance in utterances]
    )

    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1000,
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following meeting transcript in a concise manner:\n\n{transcript_text}",
            }
        ],
    )

    return response.content[0].text.strip()
