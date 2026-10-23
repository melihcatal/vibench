from google.cloud import speech
from speech_client import get_speech_client, get_gcs_uri
from speech_models import TranscriptionRequest


def submit_transcription_job(request: TranscriptionRequest):
    client = get_speech_client()
    audio = speech.RecognitionAudio(uri=request.audio_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Example, adapt to actual audio encoding
        sample_rate_hertz=16000,  # Example, adapt to actual sample rate
        language_code=request.language_code,
        enable_automatic_punctuation=True,
        enable_speaker_diarization=request.enable_speaker_diarization,
        enable_word_time_offsets=request.enable_word_time_offsets,
        model="latest_long",  # Using a specific model for batch transcription
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    print(f"Transcription job submitted. Operation name: {operation.operation.name}")
    return operation.operation.name


if __name__ == "__main__":
    # Example usage (replace with actual GCS URI)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    request = TranscriptionRequest(
        audio_uri=get_gcs_uri("your-gcs-bucket-name", "your-audio-file.wav"),
        language_code="en-US",
    )
    operation_name = submit_transcription_job(request)
    # In a real scenario, you would store this operation_name to poll later
