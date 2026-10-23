from google.cloud import speech_v1

speech_client = speech_v1.SpeechClient()

def handle_recognition_events(events):
    for event in events:
        if event.results:
            for result in event.results:
                if result.is_final:
                    print(f'Final result: {result.alternatives[0].transcript}')
                else:
                    print(f'Partial result: {result.alternatives[0].transcript}')

# Example usage:
# events = [...]  # List of recognition events
# handle_recognition_events(events)