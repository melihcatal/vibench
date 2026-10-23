import os
from google.cloud import speech_v1 as speech

def timestamped_transcript(job_name):
    client = speech.SpeechClient()
    response = client.get_operation(name=job_name).result()
    transcript = ''
    for result in response.results:
        for alternative in result.alternatives:
            transcript += alternative.transcript + ' '
            for word_info in alternative.words:
                transcript += f'[{word_info.start_time.total_seconds()}-{word_info.end_time.total_seconds()}]'
    return transcript