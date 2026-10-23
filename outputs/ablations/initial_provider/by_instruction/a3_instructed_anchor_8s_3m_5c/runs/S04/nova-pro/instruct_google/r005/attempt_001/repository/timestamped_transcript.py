from google.cloud import speech_v1 as speech

def timestamped_transcript(operation_name: str):
    client = speech.SpeechClient()
    operation = client.get_operation(name=operation_name)
    if operation.done:
        response = client.operations_v1.Operation.response(operation)
        for result in response.results:
            for alternative in result.alternatives:
                for word_info in alternative.words:
                    print(f'Word: {word_info.word}, Start Time: {word_info.start_time}, End Time: {word_info.end_time}')
    else:
        print('Transcription is still in progress.')