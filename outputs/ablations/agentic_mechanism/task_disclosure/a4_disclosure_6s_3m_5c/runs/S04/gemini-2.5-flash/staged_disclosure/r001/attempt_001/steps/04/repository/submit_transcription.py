from google.cloud import speech_v1p1beta1 as speech

def submit_transcription(gcs_uri: str):
    """Submits an audio file for batch transcription using Google Cloud Speech-to-Text.

    Args:
        gcs_uri: The Google Cloud Storage URI of the audio file to transcribe.
                 Example: "gs://cloud-samples-data/speech/brooklyn_bridge.flac"
    """

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        language_code="en-US",
        # Use a model adapted for long-form audio for batch transcription
        model="default",
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    # The result is an iteration of transcriptions. In a real application,
    # you would process these results further.
    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")
        print(f"Confidence: {result.alternatives[0].confidence}")

if __name__ == "__main__":
    # Replace with your actual GCS URI
    # This is an example from Google Cloud Speech-to-Text documentation
    # For this to work, you need to have a Google Cloud project set up
    # and authenticated (e.g., via `gcloud auth application-default login`)
    # and the service account needs permissions to read from the GCS bucket
    # and use the Speech-to-Text API.
    example_gcs_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.flac"
    submit_transcription(example_gcs_uri)
