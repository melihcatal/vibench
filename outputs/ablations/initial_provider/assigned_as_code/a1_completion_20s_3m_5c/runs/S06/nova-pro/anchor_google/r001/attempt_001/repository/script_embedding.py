from google.cloud import texttospeech


def embed_script(script):
    client = texttospeech.TextToSpeechClient()
    response = client.synthesize_speech(input=texttospeech.SynthesisInput(text=script),
        voice=texttospeech.VoiceSelectionParams(language_code="en-US"),
        audio_config=texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16))
    return response.audio_content