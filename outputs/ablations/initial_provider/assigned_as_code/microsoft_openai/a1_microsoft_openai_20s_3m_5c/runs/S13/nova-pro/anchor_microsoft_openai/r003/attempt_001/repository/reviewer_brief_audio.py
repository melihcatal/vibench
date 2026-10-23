from gtts import gTTS


def generate_brief(text):
    tts = gTTS(text=text, lang='en')
    tts.save('brief.mp3')