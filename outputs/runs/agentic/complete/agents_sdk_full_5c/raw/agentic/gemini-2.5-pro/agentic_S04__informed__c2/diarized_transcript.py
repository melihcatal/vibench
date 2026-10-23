import os
from speech_client import get_speech_client
from poll_transcription import poll_for_transcript

def request_diarized_transcript(audio_url: str):
    """
    Submits a transcription job with speaker diarization enabled
    and prints the resulting diarized transcript.

    Args:
        audio_url: The public URL of the audio file.
    """
    client = get_speech_client()
    transcriber = client.Transcriber()

    config = client.TranscriptionConfig(speaker_labels=True)

    job = transcriber.submit(audio_url, config)
    print(f"Submitted diarization job with ID: {job.id}")

    result = poll_for_transcript(job.id)

    if result.status == 'completed' and result.utterances:
        print("\nDiarized Transcript:")
        for utterance in result.utterances:
            print(f"Speaker {utterance.speaker}: {utterance.text}")
    elif result.status == 'failed':
        print(f"Diarization job failed: {result.error}")
    else:
        print("Diarization data not available in the result.")

if __name__ == '__main__':
    # An example audio file with multiple speakers
    audio_file_url = "https://storage.googleapis.com/aai-web-samples/5-speakers-2-min.wav"
    if "AUDIO_URL" in os.environ:
        audio_file_url = os.environ["AUDIO_URL"]
    
    request_diarized_transcript(audio_file_url)
