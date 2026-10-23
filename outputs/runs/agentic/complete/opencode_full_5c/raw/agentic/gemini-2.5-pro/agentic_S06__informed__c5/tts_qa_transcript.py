import os
import assemblyai as aai
from speech_models import TranscriptionRequest, TranscriptionResponse


def transcribe_qa_sample(request: TranscriptionRequest) -> TranscriptionResponse:
    """
    Transcribes a synthesized QA audio sample to verify spoken output
    using AssemblyAI.
    """
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    aai.settings.api_key = api_key

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(request.audio_path)

    if transcript.status == aai.TranscriptStatus.error:
        raise Exception(f"Transcription failed: {transcript.error}")

    return TranscriptionResponse(text=transcript.text)
