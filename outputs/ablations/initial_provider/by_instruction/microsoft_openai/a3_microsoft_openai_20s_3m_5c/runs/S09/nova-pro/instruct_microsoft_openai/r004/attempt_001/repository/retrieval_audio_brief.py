from gtts import gTTS

def retrieval_audio_brief(text: str):
    tts = gTTS(text=text, lang='en')
    tts.save('audio_brief.mp3')