from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from speech_client import create_streaming_client

client = create_streaming_client()

def stream_chunks(audio_chunks):
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
    )
    streaming_config = types.StreamingRecognitionConfig(config=config, interim_results=True)

    with client:
        for chunk in audio_chunks:
            audio = types.SpeechRecognitionAlternative(content=chunk)
            request = types.StreamingRecognizeRequest(audio_content=audio.content)
            responses = client.streaming_recognize(streaming_config, [request])
            for response in responses:
                for result in response.results:
                    print('Transcript: {}'.format(result.alternatives[0].transcript))
                    if result.is_final:
                        print('Final transcript: {}'.format(result.alternatives[0].transcript))