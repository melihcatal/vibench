import os
from google.cloud import texttospeech

def generate_audio_preview(translated_texts, output_wav_path='preview.wav'):
    """Generate a spoken preview of translated copy using Google Cloud Text-to-Speech.",
    Saves a single WAV file concatenating all segments.
    """
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text='\n'.join(translated_texts))
    voice = texttospeech.VoiceSelectionParams(
        language_code='en-US',
        name='en-US-Wavenet-D')
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    with open(output_wav_path, 'wb') as out:
        out.write(response.audio_content)
    return output_wav_path
