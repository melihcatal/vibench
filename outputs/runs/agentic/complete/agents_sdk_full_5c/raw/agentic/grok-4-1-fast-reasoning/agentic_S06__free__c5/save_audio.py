from google.cloud.texttospeech import SynthesizeSpeechResponse
from typing import Optional
import io

def save_audio(response: SynthesizeSpeechResponse,
               filename: Optional[str] = None,
               buffer: Optional[io.BytesIO] = None) -> None:
    """
    Writes synthesized speech audio from Google TTS response to a local file or buffer.
    """
    audio_content = response.audio_content
    if filename:
        with open(filename, 'wb') as f:
            f.write(audio_content)
    elif buffer is not None:
        buffer.write(audio_content)
        buffer.seek(0)
    else:
        raise ValueError('Provide either filename or buffer')
