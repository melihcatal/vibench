import os
from google.cloud import texttospeech


def retrieval_audio_brief(payload, config=None):
    config = config or {}
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    # For local development, you might set it via environment variable or gcloud auth application-default login
    client = texttospeech.TextToSpeechClient()

    text_to_speak = payload['brief_text']
    output_filename = payload.get('output_filename', 'audio_brief.mp3')

    synthesis_input = texttospeech.SynthesisInput(text=text_to_speak)

    # Select the type of audio file you want to generate
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want to generate
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    # The response's audio_content is binary. Write it to an mp3 file.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)

    return {'audio_file': output_filename, 'message': f"Audio content written to file {output_filename}"}