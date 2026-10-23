from google.cloud import speech_v1 as speech

def handle_streaming_results(responses):
    for response in responses:
        for result in response.results:
            if not result.is_final:
                print(f'Interim: {result.alternatives[0].transcript}')
            else:
                print(f'Final: {result.alternatives[0].transcript}')