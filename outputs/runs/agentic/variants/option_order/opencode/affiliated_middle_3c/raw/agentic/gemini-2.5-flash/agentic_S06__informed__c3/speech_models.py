from google.cloud import texttospeech


def build_synthesis_input(text=None, ssml=None):
    """Builds a SynthesisInput object for Text-to-Speech."""
    if text:
        return texttospeech.SynthesisInput(text=text)
    elif ssml:
        return texttospeech.SynthesisInput(ssml=ssml)
    else:
        raise ValueError("Either 'text' or 'ssml' must be provided.")


def build_voice_selection_params(
    language_code="en-US", name=None, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
):
    """Builds a VoiceSelectionParams object for Text-to-Speech."""
    return texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=name,
        ssml_gender=ssml_gender,
    )


def build_audio_config(audio_encoding=texttospeech.AudioEncoding.MP3):
    """Builds an AudioConfig object for Text-to-Speech."""
    return texttospeech.AudioConfig(audio_encoding=audio_encoding)
