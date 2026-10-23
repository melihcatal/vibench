import os
import assemblyai


def transcribe_qa_audio(audio_file_path: str):
    """
    Transcribes a synthesized QA audio sample to verify its content.
    """
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    assemblyai.settings.api_key = api_key

    transcriber = assemblyai.Transcriber()
    transcript = transcriber.transcribe(audio_file_path)

    if transcript.status == assemblyai.TranscriptStatus.error:
        return {"transcript": None, "error": transcript.error}
    else:
        return {"transcript": transcript.text, "error": None}
