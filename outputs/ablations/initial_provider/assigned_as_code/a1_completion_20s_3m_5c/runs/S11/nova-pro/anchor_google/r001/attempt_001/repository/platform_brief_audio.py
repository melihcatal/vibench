from google import texttospeech


def generate_brief_audio(output):
    tts_client = texttospeech.Client()
    input_text = texttospeech.types.SynthesisInput(text=output["text"])
    voice = texttospeech.types.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)
    audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)
    response = tts_client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
    return {"audio_content": response.audio_content}