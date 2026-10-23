from typing import List, Dict
import os
from google.cloud import texttospeech
from pydantic import BaseModel


class AudioBriefResult(BaseModel):
    audio_content: bytes
    output_file: str


def initialize_tts_client():
    """
    Initializes the Google Cloud Text-to-Speech client.

    Returns:
        Configured Google Cloud Text-to-Speech client.
    """
    return texttospeech.TextToSpeechClient()


def generate_spoken_brief(
    search_results: List[Dict[str, str]], output_file: str = "brief.mp3"
) -> AudioBriefResult:
    """
    Generates a spoken brief from retrieved search results using Google Cloud Text-to-Speech.

    Args:
        search_results: List of dictionaries containing document snippets or summaries.
        output_file: Output file path for the audio brief.

    Returns:
        AudioBriefResult containing the audio content and output file path.
    """
    client = initialize_tts_client()

    # Combine search results into a single text
    brief_text = "Here are the top results: " + ". ".join(
        [
            f"Result {idx + 1}: {result.get('snippet', '')}"
            for idx, result in enumerate(search_results)
        ]
    )

    synthesis_input = texttospeech.SynthesisInput(text=brief_text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", name="en-US-Wavenet-D"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_file, "wb") as out:
        out.write(response.audio_content)

    return AudioBriefResult(
        audio_content=response.audio_content, output_file=output_file
    )
