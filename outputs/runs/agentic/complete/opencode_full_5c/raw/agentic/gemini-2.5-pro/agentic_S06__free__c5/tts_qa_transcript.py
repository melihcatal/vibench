import os
import assemblyai as aai


def tts_qa_transcript(audio_file_path: str):
    """
    Transcribes a synthesized QA audio sample to verify spoken output.

    Args:
        audio_file_path (str): The path to the audio file to transcribe.

    Returns:
        str: The transcribed text.
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
