from google.cloud import texttospeech


def localized_audio_preview(text, language_code):
    client = texttospeech.TextToSpeechClient()
    voice = texttospeech.VoiceSelectionParams(language_code=language_code)
    synthesis_input = texttospeech.SynthesisInput(text=text)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    return client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
