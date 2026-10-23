from google.cloud import speech_v1p1beta1 as speech

def streaming_recognize_request(config, audio):
    client = speech.SpeechClient()
    streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)
    requests = (speech.StreamingRecognizeRequest(audio_content=audio), speech.StreamingRecognizeRequest(streaming_config=streaming_config))
    return client.streaming_recognize(requests=requests)

def streaming_recognize_response(response):
    for result in response.results:
        if not result.is_final:
            continue
        transcript = result.alternatives[0].transcript
        return transcript

def normalize_transcript(transcript):
    return transcript.lower().strip()