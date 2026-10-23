from google.cloud import texttospeech

def get_default_voice_params(language_code="en-US", name="en-US-Standard-C", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE):
    return texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=name,
        ssml_gender=ssml_gender,
    )

def get_default_audio_config(audio_encoding=texttospeech.AudioEncoding.MP3):
    return texttospeech.AudioConfig(
        audio_encoding=audio_encoding
    )
