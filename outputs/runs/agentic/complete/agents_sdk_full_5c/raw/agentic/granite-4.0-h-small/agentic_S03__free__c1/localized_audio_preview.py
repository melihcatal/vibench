# [LATER-STEP] localized_audio_preview.py
import os
import tempfile
from google.cloud import texttospeech
from google.cloud.texttospeech import enums, types

def generate_audio_preview(text: str, language_code: str = 'en-US') -> str:
    """Create a short spoken audio file for the supplied translated text."""
    client = texttospeech.TextToSpeechClient()
    input_ssynth = types.SynthesisInput(text=text)
    voice = types.VoiceSelectionParams(language_code=language_code, ssml_gender=enums.SsmlVoiceGender.NEUTRAL)
    audio_config = types.AudioConfig(audio_encoding=enums.AudioEncoding.MP3)
    response = client.synthesize_speech(input=input_ssynth, voice=voice, audio_config=audio_config)
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp:
        tmp.write(response.audio_content)
        return tmp.name  # Caller can read or delete the file

# Example usage
if __name__ == '__main__':
    sample = 'Bonjour le monde'
    mp3_path = generate_audio_preview(sample, language_code='fr-FR')
    print('Audio preview written to', mp3_path)
