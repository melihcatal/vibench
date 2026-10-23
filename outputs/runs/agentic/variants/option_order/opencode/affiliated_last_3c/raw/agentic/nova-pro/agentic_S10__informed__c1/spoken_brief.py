from google.cloud import texttospeech


def generate_speech(text):
    client = texttospeech.TextToSpeechClient.from_service_account_json(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )
    input_text = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )
    return response.audio_content
