from gtts import gTTS


def reviewer_brief_audio(payload, config=None):
    config = config or {}
    tts = gTTS(text=payload['text'], lang='en')
    tts.save('reviewer_brief.mp3')
    return {'audio_file': 'reviewer_brief.mp3'}