from transformers import pipeline

def reviewer_brief_audio(text):
    tts = pipeline('text-to-speech', model='facebook/fastspeech2-en-ljspeech')
    audio = tts(text)
    return audio['path']