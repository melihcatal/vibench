import os
from google.cloud import texttospeech
from model_models import LLMResponse


def generate_spoken_brief(
    llm_response: LLMResponse, output_filename: str = "spoken_brief.mp3"
):  # type: ignore
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=llm_response.text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
    return {
        "message": f"Audio content written to file {output_filename}",
        "filename": output_filename,
    }
