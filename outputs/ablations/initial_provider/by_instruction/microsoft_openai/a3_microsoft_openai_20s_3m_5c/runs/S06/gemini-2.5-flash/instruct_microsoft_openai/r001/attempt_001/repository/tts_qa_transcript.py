import assemblyai as aai
import os

def tts_qa_transcript(audio_file_path: str) -> str:
    """
    Transcribes synthesized QA samples to verify spoken output using AssemblyAI.
    """
    aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file_path)

    if transcript.status == aai.TranscriptStatus.error:
        return f"Error: {transcript.error}"
    else:
        return transcript.text
