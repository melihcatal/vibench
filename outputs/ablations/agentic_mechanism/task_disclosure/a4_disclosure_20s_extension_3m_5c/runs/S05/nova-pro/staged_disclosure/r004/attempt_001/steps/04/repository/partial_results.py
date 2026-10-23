from google.cloud import speech_v1p1beta1 as speech

def handle_streaming_recognition(response):
    if response.results:
        for result in response.results:
            if result.is_final:
                print(f"Final result: {result.alternatives[0].transcript}")
            else:
                print(f"Partial result: {result.alternatives[0].transcript}")