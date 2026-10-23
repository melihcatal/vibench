# [SAME-SCENARIO] poll_transcription.py
# Polls a batch transcription job and returns the completed transcript using Azure AI Speech SDK

import os
import azure.cognitiveservices.speech as speechsdk

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION", "eastus")

if not AZURE_SPEECH_KEY:
    raise RuntimeError("AZURE_SPEECH_KEY environment variable not set")


def poll_transcription(job_id: str) -> str:
    """Polls the transcription service until the job is complete and returns the transcript text.
    """
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
    transcription_client = speechsdk.transcription.TranscriptionClient(speech_config)

    # Wait for completion (simple poll loop)
    result = transcription_client.get_transcription_result(job_id)
    while result.status != speechsdk.transcription.TranscriptionStatus.Completed:
        # Optional: sleep or backoff strategy
        result = transcription_client.get_transcription_result(job_id)

    return result.transcript_text

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: poll_transcription.py <job_id>")
        sys.exit(1)
    transcript = poll_transcription(sys.argv[1])
    print("Transcript:")
    print(transcript)
