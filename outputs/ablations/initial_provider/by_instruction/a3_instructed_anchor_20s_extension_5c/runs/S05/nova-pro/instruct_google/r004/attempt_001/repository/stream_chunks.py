from speech_client import create_speech_client
from speech_models import create_streaming_config

def stream_chunks():
    client = create_speech_client()
    config = create_streaming_config(language_code='en-US', enable_automatic_punctuation=True)
    # Simulate streaming chunks from an async source
    for i in range(5):
        audio_content = b'simulated_audio_chunk'
        audio = types.RecognitionAudio(content=audio_content)
        request = types.StreamingRecognizeRequest(audio_content=audio)
        responses = client.streaming_recognize(config=config, requests=[request])
        for response in responses:
            for result in response.results:
                print('Transcript: {}'.format(result.alternatives[0].transcript))