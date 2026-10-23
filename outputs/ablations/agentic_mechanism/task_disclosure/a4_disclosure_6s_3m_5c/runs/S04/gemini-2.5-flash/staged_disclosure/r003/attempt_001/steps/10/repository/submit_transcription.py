
from google.cloud import speech_v1p1beta1 as speech

def submit_transcription(gcs_uri: str):
    """Submits an audio file for batch transcription using Google Cloud Speech-to-Text."""
    # Google Cloud Speech-to-Text is the concrete external provider.
    client = speech.SpeechClient()

    audio = {"uri": gcs_uri}
    config = {
        "encoding": speech.RecognitionConfig.AudioEncoding.FLAC,  # Example encoding
        "sample_rate_hertz": 16000,  # Example sample rate
        "language_code": "en-US",
        "enable_automatic_punctuation": True,
    }

    operation = client.long_running_recognize(config=config, audio=audio)

    print(f"Waiting for operation to complete...\nOperation name: {operation.operation.name}")
    response = operation.result(timeout=90)  # Waits up to 90 seconds for operation to complete

    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")
        print(f"Confidence: {result.alternatives[0].confidence}")

if __name__ == "__main__":
    # Replace with your Google Cloud Storage URI for the audio file
    # Example: "gs://cloud-samples-data/speech/brooklyn_bridge.flac"
    audio_file_gcs_uri = "gs://your-bucket-name/your-audio-file.flac"  # <<< IMPORTANT: Update this line
    submit_transcription(audio_file_gcs_uri)
