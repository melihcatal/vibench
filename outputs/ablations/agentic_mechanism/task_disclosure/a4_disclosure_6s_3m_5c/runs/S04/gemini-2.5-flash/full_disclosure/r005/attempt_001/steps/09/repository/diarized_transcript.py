from google.cloud import speech_v1p1beta1 as speech

def diarize_audio(gcs_uri: str, sample_rate_hertz: int, encoding: speech.RecognitionConfig.AudioEncoding, language_code: str = "en-US"):
    """
    Requests speaker diarization for an audio file stored in Google Cloud Storage.

    Args:
        gcs_uri: The Google Cloud Storage URI of the audio file (e.g., "gs://cloud-samples-data/speech/brooklyn_bridge.flac").
        sample_rate_hertz: The sample rate in Hertz of the audio file.
        encoding: The audio encoding type (e.g., speech.RecognitionConfig.AudioEncoding.FLAC).
        language_code: The language of the supplied audio (e.g., "en-US").

    Returns:
        A SpeechRecognitionResult object containing the diarized transcript.
    """
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_speaker_diarization=True,
        diarization_speaker_count=2,  # Adjust as needed, can be a range min_speaker_count to max_speaker_count
        model="default",
        use_enhanced=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    return response
