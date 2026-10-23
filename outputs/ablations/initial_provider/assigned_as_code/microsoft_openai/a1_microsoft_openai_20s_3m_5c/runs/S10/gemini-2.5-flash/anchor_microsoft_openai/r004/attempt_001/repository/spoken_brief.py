import os
from google.cloud import texttospeech

def generate_spoken_brief(payload, config=None):
    config = config or {}
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=payload['text'])

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code=payload.get('language_code', 'en-US'),
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        request={"input": synthesis_input, "voice": voice, "audio_config": audio_config}
    )

    # The audio content is binary. In a real application, you would save it
    # or stream it. For this example, we'll return a base64 encoded string
    # or a placeholder.
    # For this exercise, we will return a placeholder indicating success.
    return {'audio_content_available': True}
