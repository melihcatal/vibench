from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
import io
import os

def stream_microphone_audio():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    client = speech.SpeechClient()

    config = types.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_automatic_punctuation=True,
        model='phone_call'
    )

    streaming_config = types.StreamingRecognitionConfig(
        config=config,
        interim_results=True
    )

    with io.BytesIO() as audio_buffer:
        while True:
            # Simulate reading audio data from microphone
            audio_chunk = b'simulated_audio_data'
            audio_buffer.write(audio_chunk)
            request = types.StreamingRecognizeRequest(
                audio_content=audio_buffer.getvalue()
            )
            responses = client.streaming_recognize(requests=[request])
            for response in responses:
                for result in response.results:
                    print(f'Transcript: {result.alternatives[0].transcript}')
                    if result.is_final:
                        return
            audio_buffer.seek(0)
            audio_buffer.truncate()

if __name__ == '__main__':
    stream_microphone_audio()