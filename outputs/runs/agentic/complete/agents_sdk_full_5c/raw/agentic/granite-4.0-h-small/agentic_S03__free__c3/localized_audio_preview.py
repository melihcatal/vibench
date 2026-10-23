import os
import tempfile
import subprocess
from google.cloud import texttospeech

def generate_spoken_previews(translated_texts: list[str], language_code: str = 'es') -> list[str]:
    """Generate spoken (audio) previews of translated strings using Google Cloud Text-to-Speech.",
    """
    client = texttospeech.TextToSpeechClient()
    audio_configs = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    output_files = []
    with tempfile.TemporaryDirectory() as tmpdirname:
        for i, text in enumerate(translated_texts):
            synthesis_input = texttospeech.SynthesisInput(text=text)
            voice = texttospeech.VoiceSelectionParams(language_code=language_code, name='en-US-Standard-C')
            response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_configs)
            audio_file = os.path.join(tmpdirname, f'preview_{i}.mp3')
            with open(audio_file, 'wb') as out:
                out.write(response.audio_content)
            output_files.append(audio_file)
    return output_files