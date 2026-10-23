from google.cloud import texttospeech

def create_synthesis_input(text):
    return texttospeech.SynthesisInput(text=text)

def create_voice_selection_params(language_code, gender):
    return texttospeech.VoiceSelectionParams(language_code=language_code, ssml_gender=gender)

def create_audio_config(encoding):
    return texttospeech.AudioConfig(audio_encoding=encoding)