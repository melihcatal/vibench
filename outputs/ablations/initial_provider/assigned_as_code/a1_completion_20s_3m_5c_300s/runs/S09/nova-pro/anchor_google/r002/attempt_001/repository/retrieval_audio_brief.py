import pyttsx3

def retrieval_audio_brief(text):
    engine = pyttsx3.init()
    engine.save_to_file(text, 'audio_brief.mp3')
    engine.runAndWait()