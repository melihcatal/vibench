from google.cloud import speech_v1p1beta1 as speech

def create_speech_client():
    return speech.SpeechClient()

def normalize_transcription(transcription):
    # Placeholder for normalization logic
    return transcription.lower()

def prepare_batch_request(audio_files):
    requests = []
    for audio_file in audio_files:
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code='en-US'
        )
        audio = speech.RecognitionAudio(uri=audio_file)
        requests.append(speech.RecognizeRequest(config=config, audio=audio))
    return requests

def handle_batch_response(response):
    transcriptions = []
    for result in response.results:
        transcription = result.alternatives[0].transcript
        normalized_transcription = normalize_transcription(transcription)
        transcriptions.append(normalized_transcription)
    return transcriptions