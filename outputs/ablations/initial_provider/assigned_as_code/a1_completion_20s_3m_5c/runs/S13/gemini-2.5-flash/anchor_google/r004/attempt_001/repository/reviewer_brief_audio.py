import os
from google.cloud import texttospeech

def generate_reviewer_brief_audio(text, project_id=None):
    # The Text-to-Speech client does not directly use project_id in its constructor for authentication
    # It uses Application Default Credentials or GOOGLE_APPLICATION_CREDENTIALS environment variable.
    # However, for consistency and explicit provider signal, we'll keep project_id as a parameter
    # and assume it's part of the environment setup for ADC.
    
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the language and SSML voice type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
    response = client.synthesize_speech(
        request={
            "input": synthesis_input, "voice": voice, "audio_config": audio_config
        }
    )

    # The response's audio_content is binary. You can save it to a file or stream it.
    return response.audio_content
