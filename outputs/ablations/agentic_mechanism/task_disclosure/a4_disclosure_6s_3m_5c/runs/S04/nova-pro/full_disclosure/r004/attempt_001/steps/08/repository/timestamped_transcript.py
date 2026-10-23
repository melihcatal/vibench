import os
from google.cloud import speech_v1p1beta1 as speech

def get_timestamped_transcript(gcs_uri):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/credentials.json'
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_word_time_offsets=True
    )
    operation = client.long_running_recognize(config=config, audio=audio)
    result = operation.result(timeout=90)
    timestamped_transcript = []
    for result in result.results:
        alternative = result.alternatives[0]
        words = alternative.words
        for word_info in words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
            timestamped_transcript.append((word, start_time, end_time))
    return timestamped_transcript