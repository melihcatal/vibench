# platform_brief_audio.py
# [LATER-STEP] Generate spoken briefings from platform outputs

import os
from google.cloud import texttospeech
import os

# Initialize Google Cloud Text-to-Speech client
client = texttospeech.TextToSpeechClient()

AUDIO_OUT_PATH = os.getenv('AUDIO_OUT_PATH', 'output.mp3')
LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', 'en-US')
SPEECH_SPEED = float(os.getenv('SPEECH_SPEED', '1.0'))


def audio_from_text(text: str) -> str:
    """Synthesizes speech from plain text and writes an MP3 file.

    Returns the path to the generated audio file.
    """
    input_ssml = texttospeech.SynthesisInput(ssml=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=LANGUAGE_CODE,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=SPEECH_SPEED
    )
    response = client.synthesize_speech(input=input_ssml, voice=voice, audio_config=audio_config)
    # Write binary content to file
    with open(AUDIO_OUT_PATH, 'wb') as out_f:
        out_f.write(response.audio_content)
    return AUDIO_OUT_PATH

if __name__ == '__main__':
    # Demo: turn a dummy platform output into speech
    demo_text = 'Welcome to the platform briefing. This is a synthesized summary.'
    path = audio_from_text(f'<speak>{demo_text}</speak>')
    print(f'Audio written to {path}')
