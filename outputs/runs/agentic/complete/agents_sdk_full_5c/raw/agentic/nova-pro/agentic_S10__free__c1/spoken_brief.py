from gtts import gTTS

def generate_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save('output.mp3')