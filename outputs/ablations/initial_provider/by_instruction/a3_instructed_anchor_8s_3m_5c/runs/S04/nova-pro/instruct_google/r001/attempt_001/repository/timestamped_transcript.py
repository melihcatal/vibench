from google.cloud import speech_v1 as speech

def get_timestamped_transcript(operation_name):
    client = speech.SpeechClient()
    operation = client.get_operation(name=operation_name)
    if operation.done:
        response = operation.result()
        transcript = {}
        for result in response.results:
            for alternative in result.alternatives:
                words = alternative.words
                for word_info in words:
                    word = word_info.word
                    start_time = word_info.start_time
                    end_time = word_info.end_time
                    transcript[word] = (start_time, end_time)
        return transcript
    else:
        return 'Transcription not completed yet.'