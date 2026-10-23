from google.cloud import speech_v1 as speech


def create_streaming_request(audio_content):
    return speech.StreamingRecognizeRequest(audio_content=audio_content)


def parse_streaming_response(response):
    transcripts = []
    for result in response.results:
        transcripts.append(result.alternatives[0].transcript)
    return transcripts
