from google.cloud import speech_v1p1beta1 as speech

def create_batch_request(audio_uri, output_uri):
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
    )
    audio = speech.RecognitionAudio(uri=audio_uri)
    request = speech.BatchRecognizeRequest(
        config=config,
        audio=audio,
        output_uri=output_uri,
    )
    return request

def handle_batch_response(response):
    if response.results:
        for result in response.results:
            if result.alternatives:
                transcript = result.alternatives[0].transcript
                print(f'Transcript: {transcript}')
            else:
                print('No alternatives found.')
    else:
        print('No results found.')

def normalize_transcript(transcript):
    normalized = transcript.lower().strip()
    return normalized
