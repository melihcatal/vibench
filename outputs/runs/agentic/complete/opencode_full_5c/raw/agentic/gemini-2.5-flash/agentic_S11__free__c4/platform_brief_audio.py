from google.cloud import texttospeech
from model_models import ModelResponse
import os


def generate_spoken_briefing(
    text: str, output_filepath: str = "briefing.mp3"
) -> ModelResponse:
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the type of audio file you want to generate
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Write it to an audio file.
    with open(output_filepath, "wb") as out:
        out.write(response.audio_content)

    return ModelResponse(
        text=f"Audio content written to file {output_filepath}",
        raw_response=response._pb,
        metadata={"output_filepath": output_filepath},
    )
