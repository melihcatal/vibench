from google.cloud import speech_v1


def transcribe_qa_sample(audio_content: bytes, language_code: str = "en-US") -> str:
    client = speech_v1.SpeechClient()
    audio = speech_v1.RecognitionAudio(content=audio_content)
    config = speech_v1.RecognitionConfig(language_code=language_code, encoding=speech_v1.RecognitionConfig.AudioEncoding.MP3)
    response = client.recognize(config=config, audio=audio)
    transcripts = [result.alternatives[0].transcript for result in response.results if result.alternatives]
    return " ".join(transcripts)
