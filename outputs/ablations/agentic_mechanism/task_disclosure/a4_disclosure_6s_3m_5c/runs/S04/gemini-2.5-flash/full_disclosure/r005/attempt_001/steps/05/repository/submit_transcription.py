from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums

def submit_transcription(gcs_uri: str, language_code: str = "en-US"):
    """
    Submits an audio file for batch transcription using Google Cloud Speech-to-Text.

    Args:
        gcs_uri: The Google Cloud Storage URI of the audio file (e.g., "gs://cloud-samples-data/speech/brooklyn_bridge.flac").
        language_code: The language of the supplied audio (e.g., "en-US").

    Returns:
        The operation name if the transcription job was successfully submitted.
    """
    client = speech.SpeechClient()

    audio = {"uri": gcs_uri}
    config = {
        "enable_word_time_offsets": True,
        "language_code": language_code,
        "encoding": enums.RecognitionConfig.AudioEncoding.FLAC,  # Assuming FLAC for demonstration, adjust as needed
        "sample_rate_hertz": 16000,  # Assuming 16kHz, adjust as needed
    }

    operation = client.long_running_recognize(config, audio)
    return operation.operation.name

if __name__ == "__main__":
    # Example usage (replace with your GCS URI and language code)
    # This part will not be executed by the model but serves as an example for the user.
    # operation_name = submit_transcription("gs://cloud-samples-data/speech/brooklyn_bridge.flac", "en-US")
    # print(f"Transcription job submitted: {operation_name}")
    pass
