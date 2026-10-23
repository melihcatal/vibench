from typing import Optional
import os
from gtts import gTTS
from pydub import AudioSegment


def generate_spoken_brief(
    text: str, lang: str = "en", output_format: str = "mp3"
) -> bytes:
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save("temp_audio.mp3")

    audio = AudioSegment.from_mp3("temp_audio.mp3")
    if output_format != "mp3":
        audio = audio.export(format=output_format)
        audio_bytes = audio.read()
    else:
        with open("temp_audio.mp3", "rb") as f:
            audio_bytes = f.read()

    os.remove("temp_audio.mp3")
    return audio_bytes
