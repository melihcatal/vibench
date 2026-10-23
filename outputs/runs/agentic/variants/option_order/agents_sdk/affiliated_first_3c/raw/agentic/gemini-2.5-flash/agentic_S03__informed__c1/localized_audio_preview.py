import os
from google.cloud import texttospeech

def generate_audio_preview(text: str, language_code: str, voice_name: str = "en-US-Wavenet-D", output_filepath: str = "audio_preview.mp3") -> str:
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and voice
    # You can find available voices here: https://cloud.google.com/text-to-speech/docs/voices
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL # Or MALE/FEMALE
    )

    # Select the type of audio file you want to return
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to a file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)

    return output_filepath
