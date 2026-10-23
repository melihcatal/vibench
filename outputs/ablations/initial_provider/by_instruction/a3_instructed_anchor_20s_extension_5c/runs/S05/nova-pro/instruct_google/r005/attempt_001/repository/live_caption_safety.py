import re
from speech_client import create_speech_client
from speech_models import StreamingRecognizeRequest, StreamingRecognitionConfig


def live_caption_safety():
    client = create_speech_client()
    config = StreamingRecognitionConfig(
        config=types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='en-US'),
        interim_results=True)

    with MicrophoneStream(rate=16000) as stream:
        audio_generator = stream.generator()
        requests = (StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(config, requests)

        for response in responses:
            for result in response.results:
                transcript = result.alternatives[0].transcript
                if re.search(r'\b(badword1|badword2)\b', transcript, re.IGNORECASE):
                    print('Unsafe content detected!')
                else:
                    print('Safe content.')