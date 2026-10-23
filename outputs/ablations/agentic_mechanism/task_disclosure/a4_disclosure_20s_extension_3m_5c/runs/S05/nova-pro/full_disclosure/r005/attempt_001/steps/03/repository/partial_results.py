from google.cloud import speech_v1p1beta1 as speech

def handle_streaming_recognition(response):
    for result in response.results:
        if result.is_final:
            print('Final result:', result.alternatives[0].transcript)
        else:
            print('Partial result:', result.alternatives[0].transcript)