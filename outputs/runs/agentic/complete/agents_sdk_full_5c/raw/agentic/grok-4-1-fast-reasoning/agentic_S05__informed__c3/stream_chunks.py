from google.cloud import speech
from speech_client import get_speech_client
from speech_models import get_streaming_config, SpeechResult

def stream_chunks(audio_chunks):
    client = get_speech_client()
    streaming_config = get_streaming_config()
    def generate_requests():
        for content in audio_chunks:
            yield speech.StreamingRecognizeRequest(audio_content=content)
    responses = client.streaming_recognize(streaming_config, generate_requests())
    for response in responses:
        for result in response.results:
            yield SpeechResult(result.alternatives[0].transcript, result.is_final)
