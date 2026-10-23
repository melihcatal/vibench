import os
from google.cloud import texttospeech

def spoken_brief(payload, config=None):
    config = config or {}
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=payload['text'])

    # Build the voice request, select the language code (e.g., "en-US") and the ssml
    # voice gender (e.g., "neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code=config.get('language_code', 'en-US'),
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    # The response's audio_content is binary. In a real scenario, you'd save it to a file or stream it.
    # For this task, we'll return a base64 encoded string of the audio content.
    import base64
    audio_base64 = base64.b64encode(response.audio_content).decode('utf-8')

    return {'audio_content_base64': audio_base64, 'text': payload['text']}
