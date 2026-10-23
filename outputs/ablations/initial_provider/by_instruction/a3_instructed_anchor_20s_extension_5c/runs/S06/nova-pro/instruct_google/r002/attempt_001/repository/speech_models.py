from google.cloud import texttospeech

def create_synthesis_input(text=None, ssml=None):
    if text:
        return texttospeech.SynthesisInput(text=text)
    elif ssml:
        return texttospeech.SynthesisInput(ssml=ssml)

def create_voice_selection_params(language_code, ssml_gender):
    return texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=ssml_gender
    )

def create_audio_config(audio_encoding):
    return texttospeech.AudioConfig(audio_encoding=audio_encoding)