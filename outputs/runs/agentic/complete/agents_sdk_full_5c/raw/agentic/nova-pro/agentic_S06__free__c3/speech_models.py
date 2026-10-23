from google.cloud import texttospeech

def create_synthesis_input(text):
    return texttospeech.SynthesisInput(text=text)

def create_voice_selection_params(language_code):
    return texttospeech.VoiceSelectionParams(language_code=language_code, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)

def create_audio_config(audio_encoding):
    return texttospeech.AudioConfig(audio_encoding=audio_encoding)