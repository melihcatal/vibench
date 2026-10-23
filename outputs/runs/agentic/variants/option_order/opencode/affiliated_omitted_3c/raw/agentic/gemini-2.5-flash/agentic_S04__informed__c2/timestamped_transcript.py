from speech_client import SpeechClient
from speech_models import TranscriptionRequest, TranscriptionResult, Word
import os
import time


def get_timestamped_transcript(audio_url: str) -> TranscriptionResult:
    client = SpeechClient()
    # Request with word_timestamps set to True
    request = TranscriptionRequest(audio_url=audio_url, word_timestamps=True)
    submission_result = client.submit_transcription(request)

    print(f"Timestamped transcription job submitted with ID: {submission_result.id}")

    # Poll the job until it's completed or an error occurs
    transcript_result = client.poll_transcription(submission_result.id)

    if transcript_result.status == "completed":
        print("Transcription with timestamps completed:")
        if transcript_result.utterances:
            for utterance in transcript_result.utterances:
                print(f"Speaker {utterance.speaker}: {utterance.text}")
                for word in utterance.words:
                    print(f"  - {word.text} ({word.start}-{word.end} ms)")
        elif transcript_result.text and hasattr(
            client.transcriber.get_transcript_by_id(submission_result.id), "words"
        ):
            # Fallback for non-diarized transcripts that still contain word objects
            transcript = client.transcriber.get_transcript_by_id(submission_result.id)
            for word in transcript.words:
                print(f"- {word.text} ({word.start}-{word.end} ms)")
        else:
            print("No word timestamps or utterances found.")
    else:
        print(
            f"Transcription job {submission_result.id} failed with status: {transcript_result.status}"
        )

    return transcript_result


if __name__ == "__main__":
    audio_file_url = os.getenv(
        "ASSEMBLYAI_AUDIO_URL",
        "https://storage.googleapis.com/aai-web-samples/espn-bears.m4a",
    )
    get_timestamped_transcript(audio_file_url)
