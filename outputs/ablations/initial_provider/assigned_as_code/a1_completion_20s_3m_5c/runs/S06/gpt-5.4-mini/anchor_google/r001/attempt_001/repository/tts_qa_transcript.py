from google.cloud import speech


def tts_qa_transcript(payload, config=None):
    payload = dict(payload or {})
    config = dict(config or {})
    client = speech.SpeechClient()
    response = client.recognize(config=speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.MP3, language_code=config.get("language_code", "en-US")), audio=speech.RecognitionAudio(content=payload.get("audio_bytes", b"")))
    transcript = ""
    if response.results:
        transcript = response.results[0].alternatives[0].transcript
    return {"transcript": transcript, "provider": "google-cloud-speech"}
