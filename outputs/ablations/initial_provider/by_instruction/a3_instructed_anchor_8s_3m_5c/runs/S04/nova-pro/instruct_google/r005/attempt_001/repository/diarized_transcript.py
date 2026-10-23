from google.cloud import speech_v1 as speech

def diarized_transcript(audio_file_path: str, output_uri: str):
    client = speech.SpeechClient()
    audio = speech.types.RecognitionAudio(uri=audio_file_path)
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_speaker_diarization=True,
        diarization_speaker_count=2,
    )
    operation = client.long_running_recognize(config=config, audio=audio)
    print(f'Submitted diarized transcription job: {operation.name}')
    return operation.name