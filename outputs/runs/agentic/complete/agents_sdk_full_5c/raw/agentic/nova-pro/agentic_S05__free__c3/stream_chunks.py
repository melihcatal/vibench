from google.cloud import speech
from speech_client import create_speech_client

client = create_speech_client()
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code='en-US',
)
streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)

def stream_chunks(audio_chunks):
    requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in audio_chunks)
    responses = client.streaming_recognize(streaming_config, requests)
    for response in responses:
        for result in response.results:
            print(result.alternatives[0].transcript)