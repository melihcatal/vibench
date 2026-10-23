from google.cloud import texttospeech

def synthesize_ssml(ssml):
    client = texttospeech.TextToSpeechClient()
    input_ssml = texttospeech.SynthesisInput(ssml=ssml)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(input_ssml, voice, audio_config)
    return response.audio_content