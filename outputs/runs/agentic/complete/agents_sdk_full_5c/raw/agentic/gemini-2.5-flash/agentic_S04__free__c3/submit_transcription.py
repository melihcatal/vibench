from speech_client import get_speech_client
from speech_models import create_batch_recognize_config, create_recognition_audio

def submit_transcription_job(gcs_uri: str, language_code: str = 'en-US') -> str:
    """Submits an audio file for batch transcription to Google Cloud Speech-to-Text.

    Args:
        gcs_uri: The Google Cloud Storage URI of the audio file (e.g., "gs://cloud-samples-data/speech/brooklyn_bridge.flac").
        language_code: The BCP-47 language tag for the audio file.

    Returns:
        The name of the long-running operation for the transcription job.
    """
    client = get_speech_client()
    audio = create_recognition_audio(gcs_uri)
    config = create_batch_recognize_config(language_code=language_code)

    print(f"Submitting transcription job for: {gcs_uri}...")
    operation = client.longrunning_recognize(config=config, audio=audio)
    print(f"Transcription job submitted. Operation name: {operation.operation.name}")
    return operation.operation.name

# Example usage (would typically be run from a separate script or main block)
# if __name__ == "__main__":
#     # Replace with your actual GCS URI
#     audio_gcs_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.flac"
#     op_name = submit_transcription_job(audio_gcs_uri)
#     print(f"Operation Name: {op_name}")
