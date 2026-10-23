from google.cloud import speech_v1 as speech


def tts_qa_transcript(payload, config=None):
    config = config or {}
    client = speech.SpeechClient()
    audio_bytes = payload.get("audio_bytes", b"")
    recognition_config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.MP3, language_code=config.get("language_code", "en-US"))
    response = client.recognize(config=recognition_config, audio=speech.RecognitionAudio(content=audio_bytes))
    transcript = " ".join(result.alternatives[0].transcript for result in response.results if result.alternatives)
    return {"transcript": transcript}
