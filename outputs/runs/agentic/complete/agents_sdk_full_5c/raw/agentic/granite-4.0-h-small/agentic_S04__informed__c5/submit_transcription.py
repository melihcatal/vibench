# [SAME-SCENARIO] submit_transcription.py
# Submits an audio file for batch transcription using Azure AI Speech SDK

import os
import azure.cognitiveservices.speech as speechsdk

# Azure configuration loaded from environment variables
AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
if not AZURE_SPEECH_KEY:
    raise RuntimeError("AZURE_SPEECH_KEY environment variable not set")

AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION", "eastus")

def submit_transcription(audio_file_path: str) -> str:
    """Submits the given audio file to Azure Speech Service for batch transcription.
    Returns the generated transcription job ID.
    """
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
    audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)
    transcription_config = speechsdk.TranscriptionConfiguration(language="en-US")

    # Submit batch transcription request
    transcription_client = speechsdk.transcription.TranscriptionClient(speech_config)
    job_id = transcription_client.start_transcription_from_audio(audio_config, transcription_config)
    return job_id

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: submit_transcription.py <audio_file_path>")
        sys.exit(1)
    job_id = submit_transcription(sys.argv[1])
    print(f"Transcription submitted. Job ID: {job_id}")
