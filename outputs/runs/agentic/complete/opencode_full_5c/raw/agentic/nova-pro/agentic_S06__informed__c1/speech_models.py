from google.cloud.texttospeech import types


def normalize_synthesis_input(text):
    return types.SynthesisInput(text=text)


def normalize_voice_selection(language_code, gender):
    return types.VoiceSelectionParams(
        language_code=language_code, ssml_gender=types.SsmlVoiceGender.NEUTRAL
    )


def normalize_audio_config(encoding):
    return types.AudioConfig(audio_encoding=encoding)
