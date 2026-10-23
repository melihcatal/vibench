from google.cloud import texttospeech
import os
from typing import Optional

def generate_localized_audio_preview(text: str, language_code: str, voice_name: Optional[str] = None) -> bytes:
    """Generates a spoken preview of translated copy using Google Cloud Text-to-Speech API.
    Returns audio content as bytes (e.g., MP3).
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and voice.
    # For a list of available voices, see: https://cloud.google.com/text-to-speech/docs/voices
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL # Can be MALE, FEMALE, NEUTRAL
    )
    if voice_name:
        voice_params.name = voice_name

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={
            "input": synthesis_input,
            "voice": voice_params,
            "audio_config": audio_config,
        }
    )

    # The response's audio_content is binary. You can save it to a file.
    return response.audio_content

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS)
    # translated_text_es = "Hola mundo"
    # audio_bytes = generate_localized_audio_preview(translated_text_es, "es-ES")
    #
    # # Save the audio to a file
    # with open("output.mp3", "wb") as out:
    #     out.write(audio_bytes)
    #     print('Audio content written to file "output.mp3"')
    pass
