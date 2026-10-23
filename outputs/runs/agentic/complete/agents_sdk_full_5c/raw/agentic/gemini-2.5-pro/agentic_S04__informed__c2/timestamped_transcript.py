import os
from speech_client import get_speech_client
from poll_transcription import poll_for_transcript

def request_timestamped_transcript(audio_url: str):
    """
    Submits a transcription job and retrieves word-level timestamps.

    Args:
        audio_url: The public URL of the audio file.
    """
    client = get_speech_client()
    transcriber = client.Transcriber()

    # The `word_details` parameter enables word-level timestamps
    config = client.TranscriptionConfig(word_details=True)

    job = transcriber.submit(audio_url, config)
    print(f"Submitted timestamp job with ID: {job.id}")

    result = poll_for_transcript(job.id)

    if result.status == 'completed' and result.words:
        print("\nTimestamped Transcript (Word-level):")
        for word in result.words:
            start_ms = word.start
            end_ms = word.end
            print(f"[{start_ms}ms - {end_ms}ms] {word.text}")
    elif result.status == 'failed':
        print(f"Timestamp job failed: {result.error}")
    else:
        print("Timestamp data not available in the result.")


if __name__ == '__main__':
    audio_file_url = "https://storage.googleapis.com/aai-web-samples/espn-bears.m4a"
    if "AUDIO_URL" in os.environ:
        audio_file_url = os.environ["AUDIO_URL"]
    
    request_timestamped_transcript(audio_file_url)
