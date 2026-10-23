import os
from google.cloud import texttospeech

def generate_spoken_brief(text: str, output_filepath: str = "spoken_brief.mp3") -> str:
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        name="en-US-Standard-A"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": synthesis_input, "voice": voice, "audio_config": audio_config}
    )

    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)

    return output_filepath
