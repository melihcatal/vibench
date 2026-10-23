from google.cloud import texttospeech


def build_synthesis_input(text=None, ssml=None):
    if text:
        return texttospeech.SynthesisInput(text=text)
    elif ssml:
        return texttospeech.SynthesisInput(ssml=ssml)
    return None


def build_voice_selection_params(language_code, name=None, ssml_gender=None):
    return texttospeech.VoiceSelectionParams(
        language_code=language_code, name=name, ssml_gender=ssml_gender
    )


def build_audio_config(audio_encoding, speaking_rate=None, pitch=None):
    return texttospeech.AudioConfig(
        audio_encoding=audio_encoding, speaking_rate=speaking_rate, pitch=pitch
    )
