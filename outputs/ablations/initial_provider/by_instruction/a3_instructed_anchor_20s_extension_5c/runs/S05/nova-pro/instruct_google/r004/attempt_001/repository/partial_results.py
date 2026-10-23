from speech_client import create_speech_client
from speech_models import create_streaming_config

def partial_results():
    client = create_speech_client()
    config = create_streaming_config(language_code='en-US', enable_automatic_punctuation=True)
    # Simulate streaming chunks with partial results
    for i in range(5):
        audio_content = b'simulated_audio_chunk'
        audio = types.RecognitionAudio(content=audio_content)
        request = types.StreamingRecognizeRequest(audio_content=audio)
        responses = client.streaming_recognize(config=config, requests=[request])
        for response in responses:
            for result in response.results:
                if result.is_final:
                    print('Final Transcript: {}'.format(result.alternatives[0].transcript))
                else:
                    print('Interim Transcript: {}'.format(result.alternatives[0].transcript))