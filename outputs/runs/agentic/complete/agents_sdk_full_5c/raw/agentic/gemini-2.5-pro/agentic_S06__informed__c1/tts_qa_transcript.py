import os
import assemblyai as aai


def transcribe_audio_file(audio_file_path: str) -> str:
    """
    Transcribes a synthesized QA audio sample to verify spoken output
    using the AssemblyAI API.

    Args:
        audio_file_path: The local path to the audio file.

    Returns:
        The transcribed text.
    """
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    aai.settings.api_key = api_key

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file_path)

    if transcript.status == aai.TranscriptStatus.error:
        return transcript.error
    else:
        return transcript.text
