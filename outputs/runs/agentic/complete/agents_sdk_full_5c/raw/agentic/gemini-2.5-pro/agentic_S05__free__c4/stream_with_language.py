from google.cloud import speech
from speech_client import get_speech_client, RATE

def start_stream_with_settings(audio_generator):
    """
    Starts a streaming recognition request with specific language and punctuation settings.
    """
    client = get_speech_client()

    # Configure recognition settings for Spanish with automatic punctuation.
    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="es-ES",  # Spanish (Spain)
        enable_automatic_punctuation=True,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=False,  # Punctuation works best with final results
    )

    requests = (speech.StreamingRecognizeRequest(audio_content=content) for content in audio_generator)

    print("Starting stream with language code 'es-ES' and automatic punctuation.")
    
    responses = client.streaming_recognize(streaming_config, requests)

    # Process and return final transcripts
    transcripts = []
    for response in responses:
        for result in response.results:
            if result.is_final:
                transcript = result.alternatives[0].transcript
                print(f"Received Spanish transcript: {transcript}")
                transcripts.append(transcript)
    
    return transcripts
