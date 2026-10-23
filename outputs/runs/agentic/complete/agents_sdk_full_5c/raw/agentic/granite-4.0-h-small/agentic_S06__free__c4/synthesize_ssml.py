import os
from google.cloud import texttospeech
from .speech_client import TextToSpeechClient
from .speech_models import SynthesisInput, VoiceSelectionParams, AudioConfig

client = TextToSpeechClient()

def synthesize_ssml(ssml: str, voice_name: str = None, output_path: str = "output.ogg"):
    input_ = SynthesisInput(ssml=ssml)
    voice = client.select_voice(voice_name)
    audio_config = AudioConfig(audio_encoding=AudioConfig.AudioEncoding.OGG_OPUS)
    response = client.synthesize_speech(input_, voice, audio_config)
    save_audio(response.audio_content, output_path)

def main():
    ssml = "<speak>Hello, <break time='600ms'/> world! <prosody rate='slow'>This is SSML.</prosody></speak>"
    synthesize_ssml(ssml, voice_name="en-US-Wavenet-D", output_path="hello_ssml.ogg")

if __name__ == "__main__":
    main()