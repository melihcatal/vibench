from google.cloud import texttospeech

from translation_models import normalize_text


def localized_audio_preview(text: str, language_code: str) -> dict:
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=normalize_text(text))
    voice = texttospeech.VoiceSelectionParams(language_code=normalize_text(language_code), ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    return {"provider": "google", "audio_content": response.audio_content}
