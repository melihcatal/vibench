from google.cloud import texttospeech_v1

def generate_brief_audio(text):
    client = texttospeech_v1.TextToSpeechClient()
    input_text = texttospeech_v1.SynthesisInput(text=text)
    voice = texttospeech_v1.VoiceSelectionParams(language_code='en-US', ssml_gender=texttospeech_v1.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech_v1.AudioConfig(audio_encoding=texttospeech_v1.AudioEncoding.MP3)
    response = client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    return response.audio_content