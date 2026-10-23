import os
from pydub import AudioSegment

def generate_audio_brief(text):
    audio = AudioSegment.from_file('path_to_text_to_speech_service')
    audio.export('output.mp3', format='mp3')
    return 'Audio brief generated.'