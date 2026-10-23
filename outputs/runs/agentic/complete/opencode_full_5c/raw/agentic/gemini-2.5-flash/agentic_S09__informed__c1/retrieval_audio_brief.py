import os
from google.cloud import texttospeech
from typing import List

# Google Cloud Text-to-Speech expects GOOGLE_APPLICATION_CREDENTIALS to be set
# or for the application to be running in a Google Cloud environment.
# For local testing, ensure GOOGLE_APPLICATION_CREDENTIALS points to your service account key file.


def generate_spoken_brief(
    text: str,
    output_filepath: str,
    language_code: str = "en-US",
    voice_name: str = "en-US-Wavenet-D",
    ssml_gender: texttospeech.SsmlVoiceGender = texttospeech.SsmlVoiceGender.NEUTRAL,
) -> str:
    """Generates a spoken audio brief from a given text using Google Cloud Text-to-Speech.

    Args:
        text: The text content for the audio brief.
        output_filepath: The path to save the generated audio file (e.g., "brief.mp3").
        language_code: The BCP-47 language code of the voice (e.g., "en-US", "es-ES").
        voice_name: The name of the voice to use (e.g., "en-US-Wavenet-D").
        ssml_gender: The gender of the voice (NEUTRAL, MALE, FEMALE).

    Returns:
        The output_filepath if the audio was successfully generated.
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
        ssml_gender=ssml_gender,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)

    return output_filepath


def retrieval_audio_brief(
    retrieved_results: List[str], brief_filename: str = "retrieval_brief.mp3"
) -> str:
    """Generates a spoken brief from retrieved search results.

    Args:
        retrieved_results: A list of text strings representing the retrieved search results.
        brief_filename: The filename for the output audio brief.

    Returns:
        The filename of the generated audio brief.
    """
    # Concatenate the results to form a coherent brief text
    brief_text = "Here is a summary of your retrieved search results: " + " ".join(
        retrieved_results
    )

    # You might want to use an LLM here to summarize the results more effectively
    # before sending to TTS, but for this task, direct concatenation will suffice.

    audio_file = generate_spoken_brief(brief_text, brief_filename)
    return audio_file
