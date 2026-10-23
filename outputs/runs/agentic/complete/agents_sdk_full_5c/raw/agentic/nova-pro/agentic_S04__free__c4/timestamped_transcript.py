from google.cloud import speech_v1p1beta1 as speech

def timestamped_transcript(operation_name):
    client = speech.SpeechClient()
    operation = client.get_operation(name=operation_name)
    if operation.done:
        response = operation.result()
        for result in response.results:
            for alternative in result.alternatives:
                for word_info in alternative.words:
                    print(f'{word_info.word} [{word_info.start_time.total_seconds()} - {word_info.end_time.total_seconds()}]')
    else:
        return 'Transcription not completed yet.'