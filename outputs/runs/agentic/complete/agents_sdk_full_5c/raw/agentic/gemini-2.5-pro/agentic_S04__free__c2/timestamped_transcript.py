import assemblyai
from speech_client import assemblyai_client
from speech_models import WordTimestamp, TranscriptionResult

def get_timestamped_transcript(audio_url: str) -> TranscriptionResult:
    """
    Submits an audio file for transcription and returns word-level timestamps.
    This is a simplified example that assumes the job completes quickly.

    Args:
        audio_url: The publicly accessible URL of the audio file.

    Returns:
        A TranscriptionResult object containing word-level timestamps.
    """
    # Word timestamps are enabled by default in AssemblyAI
    config = assemblyai.TranscriptionConfig()

    # Using the blocking transcribe method for simplicity.
    transcript = assemblyai_client.transcribe(audio_url, config)

    if transcript.status == 'error':
        raise Exception(f"Timestamped transcription job failed: {transcript.error}")

    word_timestamps = []
    if transcript.words:
        for word in transcript.words:
            word_timestamps.append(
                WordTimestamp(
                    text=word.text,
                    start=word.start,
                    end=word.end
                )
            )

    return TranscriptionResult(
        job_id=transcript.id,
        transcript_text=transcript.text or "",
        words=word_timestamps
    )
