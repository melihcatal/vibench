from google.cloud import speech_v1p1beta1 as speech
import io

def transcribe_audio_from_bytes(audio_bytes: bytes, language_code: str = "en-US", sample_rate_hertz: int = 16000) -> str:
    """
    Transcribes audio content from bytes using Google Cloud Speech-to-Text.

    Args:
        audio_bytes: The audio content as bytes.
        language_code: The BCP-47 language tag of the audio.
        sample_rate_hertz: The sample rate of the audio in Hertz.

    Returns:
        The transcribed text.
    """
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, # Assuming LINEAR16 or FLAC for quality
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        # For better accuracy, consider using a model adaptation or phrase hints if applicable.
        # model='default' or 'phone_call', 'video', etc.
    )

    # Synchronous speech recognition
    response = client.recognize(config=config, audio=audio)

    transcript_parts = []
    for result in response.results:
        # The first alternative is the most likely transcription
        if result.alternatives:
            transcript_parts.append(result.alternatives[0].transcript)

    return " ".join(transcript_parts)

def transcribe_audio_from_gcs(gcs_uri: str, language_code: str = "en-US", sample_rate_hertz: int = 16000) -> str:
    """
    Transcribes audio content from a Google Cloud Storage URI using Google Cloud Speech-to-Text.

    Args:
        gcs_uri: The Google Cloud Storage URI of the audio file (e.g., "gs://bucket-name/path/to/audio.flac").
        language_code: The BCP-47 language tag of the audio.
        sample_rate_hertz: The sample rate of the audio in Hertz.

    Returns:
        The transcribed text.
    """
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, # Adjust encoding based on your file type
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )

    # Asynchronous speech recognition for longer audio files
    operation = client.long_running_recognize(config=config, audio=audio)

    print(f"Waiting for operation to complete... (GCS URI: {gcs_uri})")
    response = operation.result(timeout=300) # Wait for 5 minutes

    transcript_parts = []
    for result in response.results:
        if result.alternatives:
            transcript_parts.append(result.alternatives[0].transcript)

    return " ".join(transcript_parts)
