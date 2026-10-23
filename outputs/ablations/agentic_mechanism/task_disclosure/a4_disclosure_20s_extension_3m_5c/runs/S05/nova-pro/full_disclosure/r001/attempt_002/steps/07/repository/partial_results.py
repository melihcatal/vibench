from google.cloud import speech_v1 as speech

def handle_streaming_recognition(request):
    client = speech.SpeechClient()
    response = client.streaming_recognize(request)
    for result in response:
        if result.results:
            for result in result.results:
                if result.is_final:
                    print(f"Final result: {result.alternatives[0].transcript}")
                else:
                    print(f"Partial result: {result.alternatives[0].transcript}")
