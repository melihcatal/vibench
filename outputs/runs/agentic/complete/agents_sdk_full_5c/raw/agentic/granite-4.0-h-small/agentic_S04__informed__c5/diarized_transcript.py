# [SAME-SCENARIO] diarized_transcript.py
# Requests speaker diarization for a recorded meeting using Azure AI Speech SDK

import os
import azure.cognitiveservices.speech as speechsdk

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION", "eastus")

if not AZURE_SPEECH_KEY:
    raise RuntimeError("AZURE_SPEECH_KEY environment variable not set")


def diarized_transcript(audio_file_path: str, speaker_count: int = 2) -> str:
    """Requests batch transcription with speaker diarization and returns the transcript with speaker labels.
    Uses Azure AI Speech which supports diarization via TranscriptionConfiguration.
    """
    speech_config = speechsdk.SpeechConfig(subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION)
    audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)
    transcription_config = speechsdk.TranscriptionConfiguration(language="en-US")
    transcription_config.enable_diarization = True
    transcription_config.number_of_speakers = speaker_count

    transcription_client = speechsdk.transcription.TranscriptionClient(speech_config)
    job_id = transcription_client.start_transcription_from_audio(audio_config, transcription_config)
    # Simple poll to completion (same as poll_transcription)
    result = transcription_client.get_transcription_result(job_id)
    while result.status != speechsdk.transcription.TranscriptionStatus.Completed:
        result = transcription_client.get_transcription_result(job_id)
    return result.transcript_text

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: diarized_transcript.py <audio_file_path> [speaker_count]")
        sys.exit(1)
    speaker_count = int(sys.argv[2]) if len(sys.argv) == 3 else 2
    transcript = diarized_transcript(sys.argv[1], speaker_count)
    print("Diarized transcript:")
    print(transcript)
