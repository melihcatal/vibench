from google.cloud import speech
from speech_client import get_speech_client
from speech_models import create_recognition_config, create_streaming_config

def stream_with_language(audio_chunks, sample_rate_hertz, language_code, enable_automatic_punctuation=True, model='latest_long'):
    client = get_speech_client()
    recognition_config = create_recognition_config(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        model=model,
    )
    streaming_config = create_streaming_config(recognition_config, interim_results=True)

    requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in audio_chunks)
    for response in client.streaming_recognize(config=streaming_config, requests=requests):
        for result in response.results:
            if result.alternatives:
                yield {"text": result.alternatives[0].transcript, "is_final": result.is_final}
