from google.cloud import texttospeech


def localized_audio_preview(payload, config=None):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=payload["text"])
    voice = texttospeech.VoiceSelectionParams(language_code=payload["language"])
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    return {"audio_content": response.audio_content}
