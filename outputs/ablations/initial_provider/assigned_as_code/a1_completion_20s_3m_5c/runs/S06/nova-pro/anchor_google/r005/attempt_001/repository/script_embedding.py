from google.cloud import texttospeech


def embed_script(text):
    client = texttospeech.TextToSpeechClient()
    response = client.synthesize_speech(input=texttospeech.SynthesisInput(text=text),
        voice=texttospeech.VoiceSelectionParams(language_code="en-US"),
        audio_config=texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3))
    return response.audio_content
