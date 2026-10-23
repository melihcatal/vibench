import os
import assemblyai as aai
import tempfile


def transcribe_audio(audio_bytes: bytes) -> str:
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(tmp_path)
    os.unlink(tmp_path)
    return transcript.text
