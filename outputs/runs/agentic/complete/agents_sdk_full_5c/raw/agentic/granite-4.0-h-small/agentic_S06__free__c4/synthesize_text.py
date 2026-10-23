import os
from google.cloud import texttospeech
from .speech_client import TextToSpeechClient
from .speech_models import SynthesisInput, VoiceSelectionParams, AudioConfig

client = TextToSpeechClient()

def synthesize_text(plain_text: str, voice_name: str = None, output_path: str = "output.ogg"):
    input_ = SynthesisInput(text=plain_text)
    voice = client.select_voice(voice_name)
    audio_config = AudioConfig(audio_encoding=AudioConfig.AudioEncoding.OGG_OPUS)
    response = client.synthesize_speech(input_, voice, audio_config)
    save_audio(response.audio_content, output_path)

def main():
    text = "Hello, world! This is a test of text-to-speech."
    synthesize_text(text, voice_name="en-US-Wavenet-D", output_path="hello.ogg")

if __name__ == "__main__":
    main()