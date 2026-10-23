import os
from typing import List, Dict, Any
from openai import OpenAI
from speech_models import DiarizedUtterance


def translate_transcript(
    utterances: List[DiarizedUtterance], target_language: str = "es"
) -> List[Dict[str, Any]]:
    """
    Translates completed transcript segments using OpenAI's Chat Completions API.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    translated_segments = []

    for utterance in utterances:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": f"Translate the following text to {target_language}.",
                },
                {
                    "role": "user",
                    "content": utterance.text,
                },
            ],
            max_tokens=1000,
        )
        translated_text = response.choices[0].message.content.strip()
        translated_segments.append(
            {
                "speaker": utterance.speaker,
                "original_text": utterance.text,
                "translated_text": translated_text,
                "start": utterance.start,
                "end": utterance.end,
            }
        )

    return translated_segments
