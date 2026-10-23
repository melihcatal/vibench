import os
from google.cloud import texttospeech


def retrieval_audio_brief(text, config=None):
    config = config or {}
    client = texttospeech.TextToSpeechClient(api_key=config.get('api_key') or os.environ['GOOGLE_API_KEY'])
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code='en-US', ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    return response.audio_content