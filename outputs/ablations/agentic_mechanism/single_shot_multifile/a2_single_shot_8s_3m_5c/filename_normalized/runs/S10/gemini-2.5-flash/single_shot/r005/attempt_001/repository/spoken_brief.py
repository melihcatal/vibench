import os
from google.cloud import texttospeech

def generate_audio(text: str, output_filepath: str, language_code: str = "en-US") -> None:
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": synthesis_input, "voice": voice, "audio_config": audio_config}
    )

    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)

    if not os.path.exists(output_filepath):
        raise IOError(f"Failed to save audio content to {output_filepath}")