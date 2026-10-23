from gtts import gTTS

def generate_audio_brief(text):
    tts = gTTS(text=text, lang='en')
    tts.save('audio_brief.mp3')