from google.cloud import texttospeech

def create_synthesis_input(text):
    return texttospeech.SynthesisInput(text=text)

def create_ssml_input(ssml):
    return texttospeech.SynthesisInput(ssml=ssml)

def create_voice_params(language_code):
    return texttospeech.VoiceSelectionParams(language_code=language_code, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)

def create_audio_config():
    return texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)