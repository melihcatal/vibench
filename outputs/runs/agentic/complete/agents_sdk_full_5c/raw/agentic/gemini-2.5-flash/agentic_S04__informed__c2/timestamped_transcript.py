import os
import assemblyai as aai
from speech_models import TimestampedTranscriptResult, WordTimestamp

def timestamped_transcript(job_id: str) -> TimestampedTranscriptResult or None:
    """Returns word or segment timestamps from an AssemblyAI transcription result."""
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not aai.settings.api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set.")

    transcriber = aai.Transcriber()
    transcript = transcriber.get_transcript_by_id(job_id)

    if transcript.status == aai.TranscriptStatus.completed:
        words_with_timestamps = []
        for word_info in transcript.words:
            words_with_timestamps.append(WordTimestamp(
                word=word_info.text,
                start=word_info.start,
                end=word_info.end
            ))
        return TimestampedTranscriptResult(words=words_with_timestamps, status=transcript.status.value)
    elif transcript.status == aai.TranscriptStatus.failed:
        raise Exception(f"Timestamped transcription job {job_id} failed: {transcript.error}")
    
    return TimestampedTranscriptResult(words=None, status=transcript.status.value)

if __name__ == "__main__":
    # Example usage (replace with actual job ID)
    # example_job_id = "your_assemblyai_job_id"
    # result = timestamped_transcript(example_job_id)
    # if result and result.words:
    #     for word_ts in result.words:
    #         print(f"{word_ts.word} (start: {word_ts.start}ms, end: {word_ts.end}ms)")
    pass
