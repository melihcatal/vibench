import os
from google.cloud import speech_v1 as speech

def timestamped_transcript(operation_name):
    client = speech.SpeechClient()
    response = client.get_operation(name=operation_name)
    if response.done:
        result = response.result()
        for result in result.results:
            for alternative in result.alternatives:
                print('Transcript: {}'.format(alternative.transcript))
                for word_info in alternative.words:
                    print('Word: {}, Start Time: {}, End Time: {}'.format(
                        word_info.word, word_info.start_time, word_info.end_time))
    else:
        return None