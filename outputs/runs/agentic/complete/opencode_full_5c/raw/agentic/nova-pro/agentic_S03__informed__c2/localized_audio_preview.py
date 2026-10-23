import google.cloud.texttospeech as tts


def generate_audio_preview(text):
    client = tts.TextToSpeechClient()
    input_text = tts.SynthesisInput(text=text)
    voice = tts.VoiceSelectionParams(
        language_code="en-US", ssml_gender=tts.SsmlVoiceGender.NEUTRAL
    )
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.MP3)
    response = client.synthesize_speech(
        input=input_text, voice=voice, audio_config=audio_config
    )
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
    return "output.mp3"


if __name__ == "__main__":
    print(generate_audio_preview("Hello, this is a preview of the translated text."))
