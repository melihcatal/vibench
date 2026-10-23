import os
from gtts import gTTS

def platform_brief_audio(output):
    tts = gTTS(text=output, lang='en')
    tts.save('briefing.mp3')

model = select_platform_resource()
for output in stream_platform_generation(model):
    platform_brief_audio(output)