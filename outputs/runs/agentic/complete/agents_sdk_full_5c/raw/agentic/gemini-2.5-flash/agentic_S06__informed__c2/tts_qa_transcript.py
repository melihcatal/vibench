from google.cloud import speech_v1p1beta1 as speech
import os
from typing import List

def transcribe_audio_from_gcs(gcs_uri: str, language_code: str = "en-US", sample_rate_hertz: int = 16000) -> List[str]:
    """Transcribes synthesized QA samples from a Google Cloud Storage URI to verify spoken output.

    Args:
        gcs_uri: The Google Cloud Storage URI of the audio file (e.g., "gs://cloud-samples-data/speech/brooklyn_bridge.flac").
        language_code: The BCP-47 language tag for the audio.
        sample_rate_hertz: The sample rate in Hertz of the audio data.

    Returns:
        A list of transcribed text segments.
    """
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, # Assuming common audio formats
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        # Optionally, enable enhanced models for better accuracy
        # use_enhanced=True,
        # model="default", # or "latest_long", "video", "phone_call"
    )

    # Detects speech in the audio file
    operation = client.long_running_recognize(config=config, audio=audio)

    print(f"Waiting for operation to complete (this may take a while): {operation.operation.name}")
    response = operation.result(timeout=90) # Wait for up to 90 seconds

    transcripts = []
    for result in response.results:
        # The first alternative is generally the most accurate.
        transcripts.append(result.alternatives[0].transcript)

    return transcripts

def transcribe_audio_from_bytes(audio_bytes: bytes, language_code: str = "en-US", sample_rate_hertz: int = 16000, audio_encoding: speech.RecognitionConfig.AudioEncoding = speech.RecognitionConfig.AudioEncoding.MP3) -> List[str]:
    """Transcribes synthesized QA samples from audio bytes to verify spoken output.

    Args:
        audio_bytes: The audio content as bytes.
        language_code: The BCP-47 language tag for the audio.
        sample_rate_hertz: The sample rate in Hertz of the audio data.
        audio_encoding: The audio encoding of the provided bytes (e.g., MP3, LINEAR16).

    Returns:
        A list of transcribed text segments.
    """
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=audio_encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )

    response = client.recognize(config=config, audio=audio)

    transcripts = []
    for result in response.results:
        transcripts.append(result.alternatives[0].transcript)
    return transcripts


if __name__ == '__main__':
    # Example of transcribing from GCS (requires a public audio file and GOOGLE_APPLICATION_CREDENTIALS)
    # gcs_audio_uri = "gs://cloud-samples-data/speech/corrupt_audio.mp3"
    # print(f"\nTranscribing audio from GCS: {gcs_audio_uri}")
    # transcripts = transcribe_audio_from_gcs(gcs_audio_uri, language_code="en-US", sample_rate_hertz=16000)
    # if transcripts:
    #     print("Transcription results:")
    #     for i, transcript in enumerate(transcripts):
    #         print(f"  {i+1}: {transcript}")
    # else:
    #     print("No transcription results.")

    # Example of transcribing from bytes (requires actual audio bytes)
    # For this example, we'll use dummy bytes and expect an error or empty result
    dummy_audio_bytes = b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09"
    print("\nSimulating transcription from bytes (will likely fail with dummy data):")
    try:
        transcripts_from_bytes = transcribe_audio_from_bytes(
            dummy_audio_bytes, 
            language_code="en-US", 
            sample_rate_hertz=8000, 
            audio_encoding=speech.RecognitionConfig.AudioEncoding.MP3
        )
        print(f"Transcripts from bytes: {transcripts_from_bytes}")
    except Exception as e:
        print(f"Error during simulated transcription: {e}")
