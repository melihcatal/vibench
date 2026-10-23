import google.cloud.texttospeech as tts


def create_text_input(text: str) -> tts.SynthesisInput:
    return tts.SynthesisInput(text=text)


def create_ssml_input(ssml: str) -> tts.SynthesisInput:
    return tts.SynthesisInput(ssml=ssml)


def create_voice(language_code: str, name: str = None) -> tts.VoiceSelectionParams:
    return tts.VoiceSelectionParams(language_code=language_code, name=name)


def create_audio_config() -> tts.AudioConfig:
    return tts.AudioConfig(
        audio_encoding=tts.AudioEncoding.LINEAR16, sample_rate_hertz=24000
    )
