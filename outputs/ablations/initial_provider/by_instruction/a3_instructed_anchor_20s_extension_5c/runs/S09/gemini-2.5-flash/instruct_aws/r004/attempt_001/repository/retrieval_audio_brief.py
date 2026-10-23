import os
from google.cloud import texttospeech

def generate_retrieval_audio_brief(
    brief_text: str,
    output_audio_path: str = "retrieval_brief.mp3"
) -> str:
    """
    Generates a spoken brief from retrieved search results using Google Cloud Text-to-Speech API.

    Args:
        brief_text: The text content for the audio brief.
        output_audio_path: The file path to save the generated audio (e.g., "retrieval_brief.mp3").

    Returns:
        The path to the generated audio file.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=brief_text)

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to an mp3 file.
    with open(output_audio_path, "wb") as out:
        out.write(response.audio_content)

    return output_audio_path
