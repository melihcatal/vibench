# [LATER-STEP] retrieval_audio_brief.py
# Generate a spoken brief from retrieved search results using Google Text-to-Speech

import os
from google.cloud import texttospeech
from typing import List

# Configure TTS client
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
    "GOOGLE_APPLICATION_CREDENTIALS"
)
tts_client = texttospeech.TextToSpeechClient()


def generate_audio_brief(
    retrieved_texts: List[str], output_path: str = "brief.mp3"
) -> str:
    """Create a concise spoken brief from retrieved text snippets.

    Concatenates the snippets into a single string and synthesizes speech.

    Args:
        retrieved_texts (List[str]): List of text snippets from search results.
        output_path (str): File path to write the generated .mp3 audio.

    Returns:
        str: Path to the saved audio file.
    """
    # Simple concatenation for demo purposes
    brief_text = " \n".join(retrieved_texts)
    input_ssml = texttospeech.SynthesisInput(ssml=f"<speak>{brief_text}</speak>")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
    )
    response = tts_client.synthesize_speech(
        input=input_ssml, voice=voice, audio_config=audio_config
    )
    with open(output_path, "wb") as out_file:
        out_file.write(response.audio_content)
    return output_path
