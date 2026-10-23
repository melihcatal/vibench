from google.cloud import speech_v1p1beta1 as speech

def timestamped_transcript(operation_name: str, project_id: str, location: str) -> str:
    client = speech.SpeechClient()
    operation = client.get_operation(name=operation_name)
    response = client.get_operation(name=operation_name)
    transcript = ''
    for result in response.results:
        for alternative in result.alternatives:
            transcript += ' '.join([word.word for word in alternative.words])
            for word in alternative.words:
                transcript += f' [{word.start_time.seconds}.{word.start_time.nanos // 1000000}-{word.end_time.seconds}.{word.end_time.nanos // 1000000}]'
    return transcript