import os
import assemblyai as aai

def transcribe_tts_audio(audio_path: str) -> str:
    """
    Transcribes synthesized QA samples to verify spoken output using AssemblyAI.
    """
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY not set")
    aai.settings.api_key = api_key
    config = aai.TranscriptionConfig(language_code="en")
    transcriber = aai.Transcriber(config=config)
    transcript = transcriber.transcribe(audio_path)
    if transcript.error:
        raise RuntimeError(f"Transcription error: {transcript.error}")
    return transcript.text
