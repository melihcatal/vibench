from google.cloud import texttospeech

def get_text_to_speech_client():
    """Returns a Google Cloud Text-to-Speech client."""
    return texttospeech.TextToSpeechClient()

def get_audio_config(encoding="MP3", speaking_rate=1.0, pitch=0.0):
    """Returns a configured AudioConfig object."""
    return texttospeech.AudioConfig(
        audio_encoding=getattr(texttospeech.AudioEncoding, encoding.upper()),
        speaking_rate=speaking_rate,
        pitch=pitch
    )

def get_voice_selection_params(language_code="en-US", name=None, ssml_gender=None):
    """Returns a configured VoiceSelectionParams object."""
    params = {"language_code": language_code}
    if name: params["name"] = name
    if ssml_gender: params["ssml_gender"] = getattr(texttospeech.SsmlVoiceGender, ssml_gender.upper())
    return texttospeech.VoiceSelectionParams(**params)
