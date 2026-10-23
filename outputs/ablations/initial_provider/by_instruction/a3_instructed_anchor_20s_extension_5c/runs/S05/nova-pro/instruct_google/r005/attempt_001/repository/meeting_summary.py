from speech_client import create_speech_client
from speech_models import StreamingRecognizeRequest, StreamingRecognitionConfig


def meeting_summary():
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

        transcript = ''
        for response in responses:
            for result in response.results:
                transcript += result.alternatives[0].transcript + ' '

        print('Meeting summary: {}'.format(summarize_text(transcript)))


def summarize_text(text):
    # Implement text summarization logic
    return text[:100]