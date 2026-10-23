from typing import List
from gtts import gTTS
import io
import base64


def localized_audio_preview(texts: List[str], language_codes: List[str]) -> List[str]:
    """Generate spoken previews of translated copy using Google Text-to-Speech."""
    audio_previews = []

    for text, lang in zip(texts, language_codes):
        tts = gTTS(text=text, lang=lang)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_base64 = base64.b64encode(audio_buffer.getvalue()).decode("utf-8")
        audio_previews.append(audio_base64)

    return audio_previews
