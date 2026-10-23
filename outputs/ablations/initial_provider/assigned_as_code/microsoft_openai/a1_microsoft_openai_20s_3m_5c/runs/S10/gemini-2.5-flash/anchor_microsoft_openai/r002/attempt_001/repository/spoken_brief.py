import os
from google.cloud import texttospeech

def generate_spoken_brief(payload, config=None):
    config = config or {}
    text = payload.get('text', '')
    output_filename = payload.get('output_filename', 'spoken_brief.mp3')

    if not text:
        return {'audio_generated': False, 'message': 'No text provided for spoken brief.'}

    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Select the voice and audio file type
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary. Save it to a file.
    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
        
    return {'audio_generated': True, 'output_file': output_filename, 'message': f'Audio content written to file {output_filename}'}
